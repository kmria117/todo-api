# Todo API

Backend manajemen tugas (REST API) dengan arsitektur berlapis: API -> Service -> Repository.

## Menjalankan
```
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Dokumentasi interaktif: http://127.0.0.1:8000/docs

## Test
```
pytest --cov=app
```

## Endpoint
| Method | Path | Fungsi |
|---|---|---|
| POST | /tasks | Tambah tugas |
| GET | /tasks?status=&priority= | Daftar + filter |
| GET | /tasks/{id} | Detail |
| PATCH | /tasks/{id} | Ubah |
| POST | /tasks/{id}/complete | Tandai selesai |
| DELETE | /tasks/{id} | Hapus |

## Aturan bisnis
- Judul tidak boleh kosong
- Deadline tidak boleh di masa lalu
- Tugas selesai tidak boleh diubah

## Penerapan SOLID
- **S**: router (HTTP), service (bisnis), repository (data) terpisah
- **O**: penyimpanan baru cukup menambah kelas repository
- **L**: semua `TaskRepository` bisa saling menggantikan
- **I**: `TaskReader` dan `TaskWriter` dipisah
- **D**: `TaskService` bergantung pada abstraksi, wiring di `api/dependencies.py`
