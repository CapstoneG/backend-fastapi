import json

def create_vocab_enrich_file(json_file_path, output_file_path):
    try:
        # 1. Đọc dữ liệu từ file JSON
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        narrative_lines = []
        
        print(f"Đang xử lý {len(data)} từ vựng...")

        # 2. Duyệt qua từng từ và viết văn
        for entry in data:
            word = entry.get('word', '').lower()
            definition = entry.get('definition', '')
            topic = entry.get('topic', 'General')
            
            # Bắt đầu đoạn văn
            paragraph = f"The term '{word}' is a significant concept in the field of {topic}. "
            paragraph += f"It is defined as: {definition}. "
            
            # Xử lý đồng nghĩa (Synonyms) -> Tạo Edge: is_synonym_of
            if entry.get('synonyms'):
                syns = ", ".join([f"'{s}'" for s in entry['synonyms']])
                paragraph += f"Contextually, '{word}' shares a similar meaning with {syns}, allowing them to be used interchangeably in certain situations. "
            
            # Xử lý trái nghĩa (Antonyms) -> Tạo Edge: is_antonym_of
            if entry.get('antonyms'):
                ants = ", ".join([f"'{a}'" for a in entry['antonyms']])
                paragraph += f"In contrast, it serves as an antonym to {ants}. "
            
            # Xử lý Collocations (Cụm từ đi kèm) -> Tạo Edge: commonly_used_with
            if entry.get('collocations'):
                cols = ", ".join([f"'{c}'" for c in entry['collocations']])
                paragraph += f"In standard usage, '{word}' frequently appears in collocations such as {cols}. "
            
            # Kết thúc đoạn văn và thêm dòng trống
            narrative_lines.append(paragraph)
            narrative_lines.append("") 

        # 3. Ghi ra file text kết quả
        final_content = "\n".join(narrative_lines)
        
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(final_content)
            
        print(f"XONG! File '{output_file_path}' đã được tạo thành công.")
        print("-" * 30)
        print("Mẫu nội dung 300 ký tự đầu tiên:\n")
        print(final_content[:300] + "...")

    except FileNotFoundError:
        print("Lỗi: Không tìm thấy file data_source.json. Hãy đảm bảo bạn đã tạo file này.")
    except Exception as e:
        print(f"Có lỗi xảy ra: {e}")

# --- Chạy hàm ---
# create_vocab_enrich_file('data_source.json', 'vocab_enrich.txt')
import os

files = [file for file in os.listdir("./reading_json") if file.endswith(".json")]
print(f"Tìm thấy {len(files)} tài liệu trong thư mục 'reading_json'.")

for file in files:
    print(f"\n--- Xử lý tài liệu: {file} ---")
    create_vocab_enrich_file(
        os.path.join("./reading_json", file),
        os.path.join("./reading_output", file.replace(".json", "_enrich.txt"))
    )