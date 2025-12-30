import networkx as nx
from pyvis.network import Network
import os

# --- CẤU HÌNH ĐƯỜNG DẪN ---
# Dùng r"" để tránh lỗi đường dẫn Windows
# Đảm bảo đường dẫn này trỏ đúng đến file graphml của bạn
path_to_graphml = r"D:\DoAn\python_learn\rag_storage_new\graph_chunk_entity_relation.graphml"
output_file = "lightrag_graph.html"

print(f"Dang doc file tu: {path_to_graphml}")

# 1. Load file graphml
try:
    if not os.path.exists(path_to_graphml):
        raise FileNotFoundError(f"Khong tim thay file tai: {path_to_graphml}")
        
    G = nx.read_graphml(path_to_graphml)
    print(f"Da load thanh cong. So node: {len(G.nodes)}, So canh: {len(G.edges)}")
except Exception as e:
    print(f"Loi khi doc file GraphML: {e}")
    exit()

# 2. Khởi tạo Pyvis
# notebook=False để tránh phụ thuộc vào môi trường Jupyter nếu chạy script thường
net = Network(height="750px", width="100%", notebook=False, cdn_resources='in_line')

# 3. Load dữ liệu từ NetworkX
net.from_nx(G)

# 4. Tùy chỉnh (Tùy chọn)
net.toggle_physics(True)
# net.show_buttons(filter_=['physics']) # Bỏ comment nếu muốn hiện bảng chỉnh vật lý

# --- KHẮC PHỤC LỖI UNICODE ---
# Thay vì dùng net.show(), ta dùng cách thủ công để ép encoding UTF-8
try:
    # Bước này sinh ra nội dung HTML dưới dạng chuỗi
    # Lưu ý: generate_html() trả về string
    html_content = net.generate_html(output_file)
    
    # Tự mở file và ghi với encoding utf-8
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"Xuat file thanh cong: {output_file}")
    print("Hay mo file nay bang trinh duyet (Chrome/Edge).")
    
except Exception as e:
    print(f"Loi khi ghi file HTML: {e}")