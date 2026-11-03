"""Ekspor SATRIA ke HTML statis. Tidak mengimpor db.py atau menulis SQLite sumber."""
from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import sqlite3
import zipfile


# Kolom eksplisit: akun, hash kata sandi, audit, serta berkas impor mentah tidak diekspor.
QUERIES = {
    'paket': 'SELECT no,nama,pagu,target,realisasi,ppk,kontrak,catatan,sumber,diperbarui FROM paket ORDER BY no',
    'kontrak': 'SELECT nomor,supplier,tanggal_kontrak,mulai,selesai,uraian,nilai,dibayar,sisa,status,paket_no,sumber FROM kontrak ORDER BY id',
    'anggaran': 'SELECT periode,kategori,uraian,pagu,realisasi,sisa,persen,sumber FROM anggaran ORDER BY id',
    'ikpa': 'SELECT bulan,urutan,nilai,sumber,verifikasi FROM ikpa ORDER BY urutan',
    'risiko': 'SELECT id,sasaran,risiko,dampak,pengendalian,k,d,mitigasi,pic,tenggat,status,diperbarui FROM risiko ORDER BY id',
    'milestone': 'SELECT kode,nama,tanggal,status,hasil,eviden FROM milestone ORDER BY tanggal,kode',
    'keputusan': 'SELECT waktu,pengguna,objek,opsi,dasar,tenggat FROM keputusan ORDER BY waktu DESC',
    'pengaturan': "SELECT kunci,nilai,keterangan FROM pengaturan WHERE kunci IN ('ikpa_merah','ikpa_kuning','capaian_merah','capaian_kuning','risiko_merah','risiko_kuning') ORDER BY kunci",
}


def digest(path: Path) -> str:
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def long_path(path: Path) -> Path:
    """Windows: jangan lewatkan aset bernama panjang karena batas MAX_PATH."""
    value = str(path.absolute())
    if os.name == 'nt' and not value.startswith('\\\\?\\'):
        return Path('\\\\?\\' + value)
    return path


def build(source: Path, destination: Path) -> dict:
    source = Path(str(source).removeprefix('\\\\?\\'))
    database = source / 'data' / 'satria.db'
    if not long_path(database).is_file():
        raise FileNotFoundError(f'Basis data tidak ditemukan: {database}')
    template = long_path(Path(__file__).resolve().parent / 'site')
    for name in ('index.html', 'styles.css', 'app.js', '.htaccess'):
        if not (template / name).is_file():
            raise FileNotFoundError(f'Template belum lengkap: {name}')

    # Koneksi read-only + transaksi konsisten untuk semua tabel dalam satu ekspor.
    connection = sqlite3.connect(database.resolve().as_uri() + '?mode=ro', uri=True)
    connection.row_factory = sqlite3.Row
    try:
        connection.execute('PRAGMA query_only=ON')
        connection.execute('BEGIN')
        payload = {key: [dict(row) for row in connection.execute(query)] for key, query in QUERIES.items()}
    finally:
        connection.close()
    source = long_path(source)
    destination = long_path(destination)
    now = datetime.now().astimezone()
    payload['meta'] = {
        'schema_version': 1,
        'generated_at': now.strftime('%d-%m-%Y %H:%M %z'),
        'generated_date': now.date().isoformat(),
        'mode': 'snapshot-read-only',
        'source': 'Basis data aplikasi SATRIA (SQLite)',
    }
    destination.mkdir(parents=True, exist_ok=True)
    for name in ('index.html', 'styles.css', 'app.js', '.htaccess'):
        shutil.copy2(template / name, destination / name)
    for name in ('puslitbang_logo.png', 'satria_logo.png', 'satria_favicon.png', 'hero.jpg', 'fonts/plus-jakarta-sans.woff2'):
        origin = source / 'assets' / name
        if not origin.is_file():
            raise FileNotFoundError(f'Aset tampilan tidak ditemukan: {origin}')
        target = destination / 'assets' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(origin, target)

    payload['documents'] = []
    documents = sorted((source / 'assets' / 'pilar').glob('*'))
    documents.extend(sorted(source.glob('Buku Panduan*.pdf')))
    for index, origin in enumerate(documents, 1):
        if not origin.is_file() or origin.name.startswith('~$') or origin.suffix.lower() not in ('.docx', '.pdf', '.md'):
            continue
        target = destination / 'dokumen' / f'dokumen-{index:02d}{origin.suffix.lower()}'
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(origin, target)
        payload['documents'].append({'name': origin.stem, 'type': origin.suffix[1:].lower(), 'bytes': target.stat().st_size, 'url': target.relative_to(destination).as_posix()})

    payload['gallery'] = []
    for folder, group in [('kegiatan', 'Dokumentasi kegiatan'), ('galeri', 'Visual pendukung')]:
        for index, origin in enumerate(sorted((source / 'assets' / folder).glob('*')), 1):
            if not origin.is_file() or origin.suffix.lower() not in ('.jpg', '.jpeg', '.png', '.webp'):
                continue
            target = destination / 'assets' / 'galeri' / f'{folder}-{index:02d}{origin.suffix.lower()}'
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(origin, target)
            title = origin.stem
            if '_' in title and title.split('_', 1)[0].isdigit():
                title = title.split('_', 1)[1]
            title = title.replace('_', ' ')
            payload['gallery'].append({'name': title, 'group': group, 'url': target.relative_to(destination).as_posix()})

    # data.js membuat tampilan juga bisa dibuka langsung melalui file://.
    serialized = json.dumps(payload, ensure_ascii=False, allow_nan=False, separators=(',', ':'))
    serialized = serialized.replace('<', '\\u003c').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
    data_file = destination / 'data.js'
    temp_file = destination / 'data.js.tmp'
    temp_file.write_text('window.SATRIA_DATA = ' + serialized + ';\n', encoding='utf-8')
    temp_file.replace(data_file)

    for entry in payload['documents'] + payload['gallery']:
        if not (destination / entry['url']).is_file():
            raise RuntimeError('Aset ekspor hilang: ' + entry['url'])
    archive = destination.parent / 'SATRIA-DomaiNesia-Siap-Upload.zip'
    # Hanya isi folder publik yang diarsipkan, index.html langsung pada akar ZIP.
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as bundle:
        for path in sorted(destination.rglob('*')):
            if path.is_file():
                bundle.write(path, path.relative_to(destination).as_posix())
    manifest = {key: len(payload[key]) for key in QUERIES}
    manifest.update(documents=len(payload['documents']), gallery=len(payload['gallery']))
    print(json.dumps({'hasil': str(destination), 'zip': str(archive), 'jumlah': manifest}, ensure_ascii=False, indent=2))
    return payload


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ekspor HTML SATRIA untuk hosting DomaiNesia.')
    parser.add_argument('--source', type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parent / 'public_html')
    args = parser.parse_args()
    build(args.source.resolve(), args.output.resolve())
