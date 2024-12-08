import pygame
import networkx as nx
import math

# Khởi tạo Pygame
pygame.init()

# Tạo cửa sổ Pygame
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Đồ thị tương tác với Pygame")

# Thuộc tính đồ thị
NODE_RADIUS = 20  # Bán kính đỉnh
NODE_COLOR = (135, 206, 235)  # Màu xanh dương nhạt
SELECTED_NODE_COLOR = (255, 165, 0)  # Màu cam cho đỉnh được chọn
EDGE_COLOR = (169, 169, 169)  # Màu xám cạnh
BACKGROUND_COLOR = (200, 200, 200)  # Màu nền xám nhạt

# Lớp quản lý đồ thị
class GraphManager:
    def __init__(self):
        self.graph = nx.Graph()  # Đồ thị
        self.node_positions = {}  # Vị trí các đỉnh
        self.next_node_id = 1  # ID đỉnh tiếp theo
        self.selected_nodes = []  # Danh sách đỉnh được chọn để thêm cạnh
        self.highlighted_nodes = set()  # Đỉnh được chọn để đổi màu

        # Thêm đỉnh ban đầu
        self.add_node((WIDTH // 2, HEIGHT // 2))

    def add_node(self, position):
        """Thêm một đỉnh vào đồ thị"""
        if len(self.graph.nodes) <= len(self.graph.edges) + 1:  # Đảm bảo đồ thị hợp lệ
            self.graph.add_node(self.next_node_id)
            self.node_positions[self.next_node_id] = position
            self.next_node_id += 1

    def add_edge(self, u, v):
        """Thêm một cạnh giữa hai đỉnh"""
        if u != v and not self.graph.has_edge(u, v):
            self.graph.add_edge(u, v)

    def remove_node(self, node):
        """Xóa một đỉnh khỏi đồ thị"""
        if node in self.graph.nodes:
            self.graph.remove_node(node)
            del self.node_positions[node]

    def rename_node(self, old_id, new_id):
        """Đổi tên (ID) của đỉnh"""
        if old_id in self.graph.nodes and isinstance(new_id, int) and new_id > 0:
        # Đổi tên trong đồ thị
            self.graph = nx.relabel_nodes(self.graph, {old_id: new_id})
        # Cập nhật lại vị trí trong node_positions
            self.node_positions[new_id] = self.node_positions.pop(old_id)
        
        # Cập nhật danh sách các đỉnh được chọn
        if old_id in self.selected_nodes:
            self.selected_nodes[self.selected_nodes.index(old_id)] = new_id

        # Cập nhật danh sách các đỉnh được làm nổi bật
        if old_id in self.highlighted_nodes:
            self.highlighted_nodes.remove(old_id)
            self.highlighted_nodes.add(new_id)

    def draw(self, screen):
        """Vẽ đồ thị"""
        screen.fill(BACKGROUND_COLOR)  # Làm sạch màn hình
        # Vẽ cạnh
        for u, v in self.graph.edges():
            pygame.draw.line(screen, EDGE_COLOR, self.node_positions[u], self.node_positions[v], 2)
        # Vẽ đỉnh
        for node, pos in self.node_positions.items():
            # Kiểm tra đỉnh có được chọn không
            color = SELECTED_NODE_COLOR if node in self.highlighted_nodes else NODE_COLOR
            pygame.draw.circle(screen, color, pos, NODE_RADIUS)
            # Hiển thị nhãn của đỉnh
            font = pygame.font.Font('ja-jp.ttf', 20)  # Sử dụng font từ tệp ja-jp.ttf
            label = font.render(str(node), True, (0, 0, 0))
            label_rect = label.get_rect(center=pos)
            screen.blit(label, label_rect)

# Tạo một đối tượng quản lý đồ thị
graph_manager = GraphManager()

# Tạo font hỗ trợ tiếng Việt từ tệp 'ja-jp.ttf'
font = pygame.font.Font('ja-jp.ttf', 18)

# Vòng lặp chính
running = True
dragged_node = None  # Theo dõi đỉnh bị kéo
rename_mode = False  # Kiểm tra chế độ đổi tên
input_text = ""  # Lưu trữ văn bản nhập vào cho đổi tên
while running:
    graph_manager.draw(screen)  # Vẽ đồ thị
    
    # Vẽ chú thích ở góc trái màn hình
    instructions = [
        "Chuột trái: Thêm đỉnh",
        "Chuột phải: Di chuyển đỉnh",
        "Del/Space: Xóa đỉnh",
        "R: Đổi tên đỉnh (nhập số tự nhiên)"
    ]
    y_offset = 20  # Vị trí bắt đầu vẽ chú thích theo chiều dọc
    for line in instructions:
        text = font.render(line, True, (0, 0, 0))  # Chữ đen
        screen.blit(text, (10, y_offset))  # Vẽ văn bản tại vị trí (10, y_offset)
        y_offset += 30  # Tăng khoảng cách giữa các dòng chú thích
    
    if rename_mode:
        # Hiển thị hộp nhập liệu cho tên mới
        rename_font = pygame.font.Font('ja-jp.ttf', 24)
        input_label = rename_font.render("Nhập ID mới: " + input_text, True, (0, 0, 0))
        screen.blit(input_label, (10, y_offset))
    
    pygame.display.flip()  # Hiển thị màn hình

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if event.button == 1:  # Chuột trái
                if rename_mode:
                    continue  # Nếu đang ở chế độ đổi tên, không thực hiện thao tác tạo đỉnh

                # Kiểm tra xem đỉnh nào được nhấn
                clicked_node = None
                for node, pos in graph_manager.node_positions.items():
                    # Tính toán khoảng cách giữa mouse_pos và vị trí của đỉnh
                    distance = math.sqrt((pos[0] - mouse_pos[0]) ** 2 + (pos[1] - mouse_pos[1]) ** 2)
                    if distance <= NODE_RADIUS:
                        clicked_node = node
                        break

                if clicked_node:
                    # Thêm đỉnh vào danh sách chọn cạnh
                    graph_manager.selected_nodes.append(clicked_node)
                    graph_manager.highlighted_nodes.add(clicked_node)  # Đổi màu đỉnh
                    if len(graph_manager.selected_nodes) == 2:
                        u, v = graph_manager.selected_nodes
                        graph_manager.add_edge(u, v)  # Thêm cạnh
                        graph_manager.selected_nodes = []  # Reset danh sách
                        graph_manager.highlighted_nodes.clear()  # Bỏ đổi màu
                else:
                    # Thêm đỉnh mới
                    graph_manager.add_node(mouse_pos)

            elif event.button == 3:  # Chuột phải
                # Kéo đỉnh
                for node, pos in graph_manager.node_positions.items():
                    # Tính toán khoảng cách giữa mouse_pos và vị trí của đỉnh
                    distance = math.sqrt((pos[0] - mouse_pos[0]) ** 2 + (pos[1] - mouse_pos[1]) ** 2)
                    if distance <= NODE_RADIUS:
                        dragged_node = node
                        break

        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            dragged_node = None  # Dừng kéo đỉnh

        if event.type == pygame.MOUSEMOTION and dragged_node is not None:
            # Di chuyển đỉnh đang bị kéo
            graph_manager.node_positions[dragged_node] = pygame.mouse.get_pos()

        # Xóa đỉnh khi nhấn phím Space hoặc Delete
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_DELETE:
                # Kiểm tra xem có đỉnh nào được chọn không
                if graph_manager.selected_nodes:
                    node_to_remove = graph_manager.selected_nodes[-1]  # Lấy đỉnh cuối cùng trong danh sách
                    graph_manager.remove_node(node_to_remove)  # Xóa đỉnh
                    graph_manager.selected_nodes = []  # Reset danh sách

            # Bắt đầu chế độ đổi tên nếu nhấn phím 'R'
            elif event.key == pygame.K_r:
                rename_mode = True
                input_text = ""  # Reset văn bản nhập vào

            # Kiểm tra nhập liệu
            elif rename_mode:
                if event.key == pygame.K_RETURN:
                    if input_text.isdigit():
                        new_id = int(input_text)
                        if new_id > 0:
                            # Đổi tên đỉnh cuối cùng
                            old_id = graph_manager.selected_nodes[-1]
                            graph_manager.rename_node(old_id, new_id)
                            rename_mode = False  # Thoát chế độ đổi tên
                            input_text = ""  # Reset văn bản nhập
                    else:
                        # Nếu nhập không phải số, thì không đổi tên
                        rename_mode = False
                        input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]  # Xóa ký tự cuối cùng
                else:
                    input_text += event.unicode  # Thêm ký tự vào văn bản nhập

pygame.quit()
