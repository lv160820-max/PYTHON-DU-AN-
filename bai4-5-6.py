import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk

class UngDungXuLyAnh:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng dụng Xử lý ảnh - Tương tác trực tiếp")
        self.root.geometry("1300x700")
        
        # Mảng lưu trữ trạng thái hiện tại của 3 bức ảnh trên 3 cột
        self.img_cv_cols = [None, None, None]
        
        self.tao_thanh_cong_cu_tren()
        self.tao_khu_vuc_hien_thi()

    # =======================================================
    # THIẾT KẾ GIAO DIỆN CƠ BẢN
    # =======================================================
    def tao_thanh_cong_cu_tren(self):
        top_frame = tk.Frame(self.root, pady=10)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10)

        tk.Label(top_frame, text="Bước 1: Chọn ảnh cho từng bài ➡", font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=10)

        # 3 Nút Tải Ảnh (dùng lambda để truyền đúng cột cần tải ảnh vào)
        tk.Button(top_frame, text="📂 Tải ảnh Bài 4", bg="#2196F3", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5, command=lambda: self.tai_anh(0)).pack(side=tk.LEFT, padx=10)
        tk.Button(top_frame, text="📂 Tải ảnh Bài 5", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5, command=lambda: self.tai_anh(1)).pack(side=tk.LEFT, padx=10)
        tk.Button(top_frame, text="📂 Tải ảnh Bài 6", bg="#FF9800", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5, command=lambda: self.tai_anh(2)).pack(side=tk.LEFT, padx=10)

    def tao_khu_vuc_hien_thi(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)

        self.labels_hien_thi = []
        
        # --- CỘT 1: CHỨC NĂNG BÀI 4 ---
        panel_0 = tk.LabelFrame(main_frame, text="Mục hiển thị 1 (Bài 4)", font=("Arial", 10, "bold"))
        panel_0.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        lbl_0 = tk.Label(panel_0, text="Chưa có ảnh", fg="gray", font=("Arial", 12), bg="#f0f0f0")
        lbl_0.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.labels_hien_thi.append(lbl_0)
        
        ctrl_0 = tk.Frame(panel_0)
        ctrl_0.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        tk.Button(ctrl_0, text="💾 Lưu (.png, .jpg, .bmp)", font=("Arial", 9, "bold"), command=self.bai4_luu_anh).pack(expand=True, fill=tk.X, padx=2)

        # --- CỘT 2: CHỨC NĂNG BÀI 5 ---
        panel_1 = tk.LabelFrame(main_frame, text="Mục hiển thị 2 (Bài 5)", font=("Arial", 10, "bold"))
        panel_1.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        lbl_1 = tk.Label(panel_1, text="Chưa có ảnh", fg="gray", font=("Arial", 12), bg="#f0f0f0")
        lbl_1.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.labels_hien_thi.append(lbl_1)
        
        ctrl_1 = tk.Frame(panel_1)
        ctrl_1.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        tk.Button(ctrl_1, text="☀ Tăng sáng (+15)", font=("Arial", 9, "bold"), command=self.bai5_tang_sang).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        tk.Button(ctrl_1, text="🔅 Giảm sáng (-15)", font=("Arial", 9, "bold"), command=self.bai5_giam_sang).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        # --- CỘT 3: CHỨC NĂNG BÀI 6 ---
        panel_2 = tk.LabelFrame(main_frame, text="Mục hiển thị 3 (Bài 6)", font=("Arial", 10, "bold"))
        panel_2.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        lbl_2 = tk.Label(panel_2, text="Chưa có ảnh", fg="gray", font=("Arial", 12), bg="#f0f0f0")
        lbl_2.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.labels_hien_thi.append(lbl_2)
        
        ctrl_2 = tk.Frame(panel_2)
        ctrl_2.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        tk.Button(ctrl_2, text="↻ Xoay 90°", font=("Arial", 9, "bold"), command=self.bai6_xoay).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        tk.Button(ctrl_2, text="➡ Dịch 50px", font=("Arial", 9, "bold"), command=self.bai6_dich_chuyen).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        tk.Button(ctrl_2, text="🔍 Phóng 1.5x", font=("Arial", 9, "bold"), command=self.bai6_thu_phong).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

    # =======================================================
    # HÀM HỖ TRỢ: ĐỌC ẢNH VÀ HIỂN THỊ
    # =======================================================
    def tai_anh(self, col_index):
        path = filedialog.askopenfilename(title="Chọn ảnh", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if path:
            img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
            self.img_cv_cols[col_index] = img # Lưu vào bộ nhớ tạm để chỉnh sửa
            self.hien_thi_len_gui(img, col_index)

    def hien_thi_len_gui(self, img_cv, col_index):
        img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_pil.thumbnail((400, 400)) # Chỉ thu nhỏ hình để nhét vừa khung, không ảnh hưởng file gốc
        img_tk = ImageTk.PhotoImage(img_pil)
        
        self.labels_hien_thi[col_index].configure(image=img_tk, text="")
        self.labels_hien_thi[col_index].image = img_tk

    # =======================================================
    # LOGIC BÀI 4, BÀI 5, BÀI 6 (GẮN VÀO CÁC NÚT TƯƠNG TÁC)
    # =======================================================
    def bai4_luu_anh(self):
        img = self.img_cv_cols[0]
        if img is not None:
            cv2.imwrite("bai4_anh_luu.png", img)
            cv2.imwrite("bai4_anh_luu.jpg", img)
            cv2.imwrite("bai4_anh_luu.bmp", img)
            messagebox.showinfo("Bài 4", "Đã lưu thành công 3 định dạng (.png, .jpg, .bmp) vào thư mục chứa file code!")
        else:
            messagebox.showwarning("Lỗi", "Vui lòng tải ảnh Bài 4 trước!")

    def bai5_tang_sang(self):
        img = self.img_cv_cols[1]
        if img is not None:
            M = np.ones(img.shape, dtype="uint8") * 15 # Mỗi lần nhấn tăng 15 điểm sáng
            self.img_cv_cols[1] = cv2.add(img, M)
            self.hien_thi_len_gui(self.img_cv_cols[1], 1)

    def bai5_giam_sang(self):
        img = self.img_cv_cols[1]
        if img is not None:
            M = np.ones(img.shape, dtype="uint8") * 15 # Mỗi lần nhấn giảm 15 điểm tối
            self.img_cv_cols[1] = cv2.subtract(img, M)
            self.hien_thi_len_gui(self.img_cv_cols[1], 1)

    def bai6_xoay(self):
        img = self.img_cv_cols[2]
        if img is not None:
            # Nhấn liên tục sẽ xoay mòng mòng 90 độ mỗi lần
            self.img_cv_cols[2] = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            self.hien_thi_len_gui(self.img_cv_cols[2], 2)

    def bai6_dich_chuyen(self):
        img = self.img_cv_cols[2]
        if img is not None:
            h, w = img.shape[:2]
            M_dich = np.float32([[1, 0, 50], [0, 1, 0]]) # Dịch phải 50px
            self.img_cv_cols[2] = cv2.warpAffine(img, M_dich, (w, h))
            self.hien_thi_len_gui(self.img_cv_cols[2], 2)

    def bai6_thu_phong(self):
        img = self.img_cv_cols[2]
        if img is not None:
            # Phóng to thực tế 1.5 lần vào mảng dữ liệu ảnh
            self.img_cv_cols[2] = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_LINEAR)
            self.hien_thi_len_gui(self.img_cv_cols[2], 2)

if __name__ == "__main__":
    root = tk.Tk()
    app = UngDungXuLyAnh(root)
    root.mainloop()