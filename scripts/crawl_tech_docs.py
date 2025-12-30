import os
import time
import trafilatura
from urllib.parse import urlparse

# --- CẤU HÌNH ---
OUTPUT_DIR = "./real_tech_dataset"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Danh sách 10 URL chất lượng cao (Selected Sources)
# Đây là các trang được dân IT tin dùng, nội dung rất sâu và chuẩn.
TARGET_URLS = {
    "Microservices": "https://microservices.io/patterns/microservices.html", # Nguồn gốc của khái niệm Microservices
    "Docker_Overview": "https://docs.docker.com/get-started/overview/", # Official Docker Docs
    "Apache_Kafka": "https://kafka.apache.org/intro", # Official Kafka Intro
    "REST_API": "https://aws.amazon.com/what-is/restful-api/", # AWS giải thích rất kỹ về REST
    "CI_CD": "https://www.atlassian.com/continuous-delivery/principles/continuous-integration-vs-delivery-vs-deployment", # Atlassian giải thích cực hay
    "SQL_vs_NoSQL": "https://www.mongodb.com/resources/basics/databases/nosql-explained", # MongoDB so sánh chi tiết
    "OAuth2_Auth": "https://auth0.com/intro-to-iam/what-is-oauth-2", # Auth0 giải thích về Auth
    "Kubernetes_K8s": "https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/", # Official K8s Docs
    "SOLID_Principles": "https://www.digitalocean.com/community/conceptual-articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design", # DigitalOcean giải thích SOLID
    "Git_Version_Control": "https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control" # Chương 1 của sách Pro Git
}

def crawl_and_save():
    print(f"🚀 Bắt đầu crawl dữ liệu từ {len(TARGET_URLS)} nguồn...\n")
    
    success_count = 0
    
    for topic, url in TARGET_URLS.items():
        print(f"⏳ Đang tải: {topic} ...")
        print(f"   Source: {url}")
        
        try:
            # 1. Tải HTML về
            downloaded = trafilatura.fetch_url(url)
            
            if downloaded is None:
                print(f"   ❌ Lỗi: Không truy cập được URL (Có thể do chặn Bot).")
                continue

            # 2. Trích xuất nội dung chính (Main Content Extraction)
            # include_tables=True: Lấy cả bảng so sánh (rất tốt cho RAG)
            text_content = trafilatura.extract(downloaded, include_tables=True, include_comments=False)
            
            if text_content:
                # 3. Thêm Metadata vào đầu file để LightRAG hiểu context
                header = f"Topic: {topic}\nSource: {url}\nDomain: Software Engineering/Backend\n"
                header += "="*40 + "\n\n"
                
                final_content = header + text_content
                
                # 4. Lưu file
                filename = os.path.join(OUTPUT_DIR, f"{topic}.txt")
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(final_content)
                
                # Tính sơ bộ độ dài
                word_count = len(text_content.split())
                print(f"   ✅ Thành công! Đã lưu {word_count} từ vào file '{topic}.txt'")
                success_count += 1
            else:
                print(f"   ⚠️ Cảnh báo: Không trích xuất được text từ {url}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
        
        print("-" * 50)
        # Nghỉ 1 xíu để không bị chặn IP
        time.sleep(1) 

    print(f"\n🎉 Hoàn tất! Đã lấy được {success_count}/{len(TARGET_URLS)} tài liệu.")
    print(f"📂 Kiểm tra thư mục: {os.path.abspath(OUTPUT_DIR)}")

if __name__ == "__main__":
    crawl_and_save()