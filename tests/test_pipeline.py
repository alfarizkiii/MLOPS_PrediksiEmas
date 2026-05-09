import os

def test_directories_exist():
    """Memastikan struktur direktori utama tersedia."""
    assert os.path.exists("src"), "Folder src/ tidak ditemukan!"
    assert os.path.exists("config"), "Folder config/ tidak ditemukan!"

def test_model_metadata_exists():
    """Memastikan file konfigurasi metadata sudah dibuat di LK sebelumnya."""
    assert os.path.exists("config/model_metadata.yaml"), "File metadata hilang!"