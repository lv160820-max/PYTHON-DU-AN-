import cv2
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox
import os

class UngDungXuLyAnh:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng dụng Xử lý ảnh Tổng hợp")
        self.root.geometry("1450x750")  
        
        self.img1_cv = None
        self.img2_cv = None
        self.img3_cv = None
        
        self.scale1 = 1.0
        self.scale2 = 1.0
        self.scale3 = 1.0

        # --- KHU VỰC 1: CÁC NÚT CHỨC NĂNG CHÍNH ---
        frame_chuc_nang = tk.Frame(root, pady=10)
        frame_chuc_nang.pack(side=tk.TOP, fill=tk.X)
        
        tk.Button(frame_chuc_nang, text="Chức năng 1: Gốc - Xám - HSV", command=self.chay_chuc_nang_1, font=("Arial", 11, "bold"), bg="#2196F3", fg="white", padx=10, pady=5).pack(side=tk.LEFT, padx=15)
        tk.Button(frame_chuc_nang, text="Chức năng 2: Bitwise AND (2 ảnh)", command=self.chay_chuc_nang_2, font=("Arial", 11, "bold"), bg="#4CAF50", fg="white", padx=10, pady=5).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_chuc_nang, text="Chức năng 3: Biến đổi hình học", command=self.chay_chuc_nang_3, font=("Arial", 11, "bold"), bg="#FF9800", fg="white", padx=10, pady=5).pack(side=tk.LEFT, padx=10)

        # --- KHU VỰC 2: KHUNG CHỨA 3 CỘT ẢNH ---
        self.frame_hien_thi = tk.Frame(root, bg="#f0f0f0")
        self.frame_hien_thi.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.frame_hien_thi.grid_columnconfigure(0, weight=1)
        self.frame_hien_thi.grid_columnconfigure(1, weight=1)
        self.frame_hien_thi.grid_columnconfigure(2, weight=1)
        self.frame_hien_thi.grid_rowconfigure(0, weight=1)
        
        self.tao_cot_giao_dien(0, "Mục hiển thị 1")
        self.tao_cot_giao_dien(1, "Mục hiển thị 2")
        self.tao_cot_giao_dien(2, "Mục hiển thị 3")

    def tao_cot_giao_dien(self, index, tieu_de):
        frame_cot = tk.LabelFrame(self.frame_hien_thi, text=tieu_de, font=("Arial", 11, "bold"), padx=5, pady=5)
        frame_cot.grid(row=0, column=index, sticky="nsew", padx=10, pady=5)
        
        frame_chua_anh = tk.Frame(frame_cot, width=430, height=450, bg="white")
        frame_chua_anh.pack(fill=tk.BOTH, expand=True, pady=5)
        frame_chua_anh.pack_propagate(False) 
        
        lbl_anh = tk.Label(frame_chua_anh, text="Chưa có ảnh", fg="gray", bg="white", font=("Arial", 12))
        lbl_anh.pack(fill=tk.BOTH, expand=True)
        
        frame_nut_con = tk.Frame(frame_cot)
        frame_nut_con.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        
        btn_luu = tk.Button(frame_nut_con, text="Lưu nhiều định dạng 💾", command=lambda: self.luu_anh_da_dinh_dang(index), state=tk.DISABLED, bg="#9E9E9E", fg="white", font=("Arial", 9, "bold"))
        btn_luu.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        
        btn_in = tk.Button(frame_nut_con, text="Phóng to + 🔍", command=lambda: self.zoom_anh(index, 1.2), state=tk.DISABLED)
        btn_in.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        
        btn_out = tk.Button(frame_nut_con, text="Thu nhỏ - 🔎", command=lambda: self.zoom_anh(index, 0.8), state=tk.DISABLED)
        btn_out.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        
        if not hasattr(self, 'cac_cot_gui'): self.cac_cot_gui = {}
        self.cac_cot_gui[index] = {"frame_cot": frame_cot, "lbl_anh": lbl_anh, "btn_luu": btn_luu, "btn_in": btn_in, "btn_out": btn_out}

    def chay_chuc_nang_1(self):
        file_path = filedialog.askopenfilename(title="Chọn một ảnh", filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")])
        if not file_path: return
        img = cv2.imread(file_path)
        if img is None: return
        
        self.scale1 = self.scale2 = self.scale3 = 1.0
        self.img1_cv = img.copy()
        self.img2_cv = cv2.cvtColor(cv2.cvtColor(self.img1_cv, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
        self.img3_cv = cv2.cvtColor(self.img1_cv, cv2.COLOR_BGR2HSV)
        
        self.cac_cot_gui[0]["frame_cot"].config(text="Ảnh 1: Ảnh gốc")
        self.cac_cot_gui[1]["frame_cot"].config(text="Ảnh 2: Ảnh xám")
        self.cac_cot_gui[2]["frame_cot"].config(text="Ảnh 3: Ảnh HSV")
        
        self.cap_nhat_giao_dien_anh(0, self.img1_cv, self.scale1)
        self.cap_nhat_giao_dien_anh(1, self.img2_cv, self.scale2)
        self.cap_nhat_giao_dien_anh(2, self.img3_cv, self.scale3)

    def chay_chuc_nang_2(self):
        messagebox.showinfo("Thông báo", "Vui lòng chọn ẢNH THỨ NHẤT")
        file1 = filedialog.askopenfilename(title="Chọn ảnh thứ nhất", filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if not file1: return
        messagebox.showinfo("Thông báo", "Vui lòng chọn ẢNH THỨ HAI")
        file2 = filedialog.askopenfilename(title="Chọn ảnh thứ hai", filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if not file2: return

        img1, img2 = cv2.imread(file1), cv2.imread(file2)
        if img1 is None or img2 is None: return
        
        self.scale1 = self.scale2 = self.scale3 = 1.0
        kich_thuoc_chuan = (400, 350)
        self.img1_cv = cv2.resize(img1, kich_thuoc_chuan)
        self.img2_cv = cv2.resize(img2, kich_thuoc_chuan)
        self.img3_cv = cv2.bitwise_and(self.img1_cv, self.img2_cv)
        
        self.cac_cot_gui[0]["frame_cot"].config(text="Ảnh 1: Ảnh nguồn A")
        self.cac_cot_gui[1]["frame_cot"].config(text="Ảnh 2: Ảnh nguồn B")
        self.cac_cot_gui[2]["frame_cot"].config(text="Ảnh 3: Kết quả Bitwise AND")
        
        self.cap_nhat_giao_dien_anh(0, self.img1_cv, self.scale1)
        self.cap_nhat_giao_dien_anh(1, self.img2_cv, self.scale2)
        self.cap_nhat_giao_dien_anh(2, self.img3_cv, self.scale3)

    def chay_chuc_nang_3(self):
        file_path = filedialog.askopenfilename(title="Chọn một ảnh để biến đổi", filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")])
        if not file_path: return
        img_goc = cv2.imread(file_path)
        if img_goc is None: return
        
        self.scale1 = self.scale2 = self.scale3 = 1.0
        h, w = img_goc.shape[:2]
        self.img1_cv = cv2.rotate(img_goc, cv2.ROTATE_90_CLOCKWISE)
        M = np.float32([[1, 0, 50], [0, 1, 0]])
        self.img2_cv = cv2.warpAffine(img_goc, M, (w + 50, h), borderValue=(255, 255, 255))
        self.img3_cv = cv2.resize(img_goc, (int(w * 1.5), int(h * 1.5)), interpolation=cv2.INTER_LINEAR)

        self.cac_cot_gui[0]["frame_cot"].config(text="Ảnh 1: Xoay 90 độ 🔄")
        self.cac_cot_gui[1]["frame_cot"].config(text="Ảnh 2: Dịch phải 50px ➡️")
        self.cac_cot_gui[2]["frame_cot"].config(text="Ảnh 3: Phóng to 1.5x 🔎")

        self.cap_nhat_giao_dien_anh(0, self.img1_cv, self.scale1)
        self.cap_nhat_giao_dien_anh(1, self.img2_cv, self.scale2)
        self.cap_nhat_giao_dien_anh(2, self.img3_cv, self.scale3)

    def cap_nhat_giao_dien_anh(self, index, anh_cv, scale_factor):
        if anh_cv is None: return
        h_goc, w_goc = anh_cv.shape[:2]
        chieu_cao_co_so = 380
        ty_le_co_gian = chieu_cao_co_so / h_goc
        chieu_rong_co_so = int(w_goc * ty_le_co_gian)
        
        w_final = max(int(chieu_rong_co_so * scale_factor), 50)
        h_final = max(int(chieu_cao_co_so * scale_factor), 50)
        
        anh_xem_tam = cv2.resize(anh_cv, (w_final, h_final))
        anh_rgb = cv2.cvtColor(anh_xem_tam, cv2.COLOR_BGR2RGB)
        img_pillow = Image.fromarray(anh_rgb)
        photo_img = ImageTk.PhotoImage(image=img_pillow)
        
        if not hasattr(self, 'bo_nho_anh'): self.bo_nho_anh = {}
        self.bo_nho_anh[index] = photo_img
        
        cot = self.cac_cot_gui[index]
        cot["lbl_anh"].config(image=photo_img, text="")
        cot["btn_luu"].config(state=tk.NORMAL, bg="#E91E63") 
        cot["btn_in"].config(state=tk.NORMAL)
        cot["btn_out"].config(state=tk.NORMAL)

    def zoom_anh(self, index, he_so_nhan):
        if index == 0:
            self.scale1 = max(min(self.scale1 * he_so_nhan, 3.0), 0.3)
            self.cap_nhat_giao_dien_anh(0, self.img1_cv, self.scale1)
        elif index == 1:
            self.scale2 = max(min(self.scale2 * he_so_nhan, 3.0), 0.3)
            self.cap_nhat_giao_dien_anh(1, self.img2_cv, self.scale2)
        elif index == 2:
            self.scale3 = max(min(self.scale3 * he_so_nhan, 3.0), 0.3)
            self.cap_nhat_giao_dien_anh(2, self.img3_cv, self.scale3)

    def luu_anh_da_dinh_dang(self, index):
        anh_can_luu = [self.img1_cv, self.img2_cv, self.img3_cv][index]
        if anh_can_luu is None: return
        
        duong_dan_co_so = filedialog.asksaveasfilename(title="Nhập tên tệp cần lưu", defaultextension=".png", filetypes=[("All Files", "*.*")])
        if duong_dan_co_so:
            ten_file_goc, _ = os.path.splitext(duong_dan_co_so)
            try:
                cv2.imwrite(ten_file_goc + ".png", anh_can_luu)
                cv2.imwrite(ten_file_goc + ".jpg", anh_can_luu, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
                cv2.imwrite(ten_file_goc + ".bmp", anh_can_luu)
                messagebox.showinfo("Thành công", "Đã tự động xuất đủ 3 file: .PNG, .JPG, .BMP")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu file: {str(e)}")

if __name__ == "__main__":
    giao_dien = tk.Tk()
    app = UngDungXuLyAnh(giao_dien)
    giao_dien.mainloop()
