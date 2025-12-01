import boto3
import os
from datetime import datetime
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv

# --- CẤU HÌNH ---
# 1. Load biến môi trường từ file .env 
# Lấy đường dẫn tuyệt đối của file .env để Crontab không bị lỗi
script_dir = os.path.dirname(os.path.abspath(__file__))

load_dotenv(os.path.join(script_dir, '../.env'))

MINIO_ENDPOINT = 'http://localhost:9000'
ACCESS_KEY = os.getenv('MINIO_ROOT_USER', 'admin') 
SECRET_KEY = os.getenv('MINIO_ROOT_PASSWORD', 'password123') 
BUCKET_NAME = 'backup-files'

# 2. Khởi tạo Client
s3 = boto3.client('s3',
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name='us-east-1'
)

def upload_to_minio(local_file, bucket_name, s3_file):
    try:
        s3.upload_file(local_file, bucket_name, s3_file)
        print(f" Upload thanh cong: {local_file} -> {bucket_name}/{s3_file}")
        return True
    except FileNotFoundError:
        print(" File khong tim thay")
        return False
    except NoCredentialsError:
        print(" Sai thong tin dang nhap")
        return False
    except Exception as e:
        print(f" Loi khac: {e}")
        return False

# --- PHẦN CHẠY CHÍNH ---
if __name__ == "__main__":
    # 3. Tạo file dữ liệu mẫu kèm thời gian 
    # Định dạng: db_dump_Năm-Tháng-Ngày_Giờ-Phút-Giây.txt
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    local_filename = f"db_dump_{now}.txt"
    # Lưu vào thư mục con 'daily_backups' trên MinIO 
    s3_filename = f"daily_backups/db_dump_{now}.txt"

    # Tạo nội dung mẫu
    with open(local_filename, "w") as f:
        f.write(f"Du lieu backup tu dong luc {now}\n")
        f.write("Day la du lieu quan trong can luu tru.")

    print(f" Dang backup file: {local_filename}...")

    # 4. Upload lên MinIO
    success = upload_to_minio(local_filename, BUCKET_NAME, s3_filename)

    # 5. Dọn dẹp (Xóa file local sau khi upload xong để tiết kiệm ổ cứng)
    if success:
        if os.path.exists(local_filename):
            os.remove(local_filename)
            print(" Da don dep file local.")
    else:
        print("  Giu lai file local do upload that bai.")
