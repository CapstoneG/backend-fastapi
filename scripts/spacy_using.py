import spacy

# 1. Tải mô hình ngôn ngữ tiếng Anh (nhẹ, miễn phí)
# Cần chạy lệnh: python -m spacy download en_core_web_sm trước
nlp = spacy.load("en_core_web_sm")

def extract_keywords(text):
    doc = nlp(text)
    keywords = []
    
    # Các loại từ muốn giữ lại
    target_pos = ["NOUN", "PROPN", "VERB", "ADJ"]
    
    for token in doc:
        # Điều kiện lọc:
        # 1. Không phải là stop word (is, the, at...)
        # 2. Không phải là dấu câu (., ?, !)
        # 3. Thuộc nhóm từ loại quan trọng (Noun, Verb, Adj)
        if not token.is_stop and not token.is_punct and token.pos_ in target_pos:
            # Lấy dạng nguyên thể (lemma) để tránh trùng lặp 
            # (ví dụ: "negotiated" -> "negotiate")
            keywords.append(token.lemma_.lower())
            
    # Xóa trùng lặp bằng set
    return list(set(keywords))

# --- Thử nghiệm ---
import os
files = [file for file in os.listdir("./reading_topic") if file.endswith(".txt")]
print(f"Tìm thấy {len(files)} tài liệu trong thư mục 'reading_topic'.")

for file in files:
    with open(os.path.join("./reading_topic", file), "r", encoding="utf-8") as f:
        reading_text = f.read()
    
    print(f"\n--- Phân tích tài liệu: {file} ---")
    extracted_words = extract_keywords(reading_text)

    print(f"Tổng số từ gốc: {len(reading_text.split())}")
    print(f"Số từ khóa quan trọng giữ lại: {len(extracted_words)}")
    print("-" * 20)
    print(extracted_words)