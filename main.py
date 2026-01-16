import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from blind_watermark import WaterMark


class WatermarkApp:
    def __init__(self, master):
        self.master = master
        master.title("ShadowMark")
        master.geometry("500x400")
        master.resizable(False, False)

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        self.embed_frame = ttk.Frame(self.notebook, padding=20)
        self.extract_frame = ttk.Frame(self.notebook, padding=20)

        self.notebook.add(self.embed_frame, text="嵌入水印")
        self.notebook.add(self.extract_frame, text="提取水印")

        self._build_embed_ui()
        self._build_extract_ui()

        self.original_path = None
        self.embedded_path = None

    def _build_embed_ui(self):
        frame = self.embed_frame

        ttk.Label(frame, text="原图:").grid(row=0, column=0, sticky='e', pady=5)
        self.embed_file_label = ttk.Label(frame, text="未选择", width=35)
        self.embed_file_label.grid(row=0, column=1, pady=5, padx=5)
        ttk.Button(frame, text="选择", command=self._select_original).grid(row=0, column=2, pady=5)

        ttk.Label(frame, text="水印文本:").grid(row=1, column=0, sticky='e', pady=5)
        self.wm_text_entry = ttk.Entry(frame, width=40)
        self.wm_text_entry.grid(row=1, column=1, columnspan=2, pady=5, sticky='w')

        ttk.Label(frame, text="密码:").grid(row=2, column=0, sticky='e', pady=5)
        self.embed_pwd_entry = ttk.Entry(frame, width=20)
        self.embed_pwd_entry.grid(row=2, column=1, pady=5, sticky='w')

        ttk.Button(frame, text="嵌入并保存", command=self._embed_watermark).grid(row=3, column=1, pady=20)

        self.embed_info = ttk.Label(frame, text="", foreground="blue")
        self.embed_info.grid(row=4, column=0, columnspan=3, pady=10)

    def _build_extract_ui(self):
        frame = self.extract_frame

        ttk.Label(frame, text="隐写图:").grid(row=0, column=0, sticky='e', pady=5)
        self.extract_file_label = ttk.Label(frame, text="未选择", width=35)
        self.extract_file_label.grid(row=0, column=1, pady=5, padx=5)
        ttk.Button(frame, text="选择", command=self._select_embedded).grid(row=0, column=2, pady=5)

        ttk.Label(frame, text="水印长度:").grid(row=1, column=0, sticky='e', pady=5)
        self.wm_shape_entry = ttk.Entry(frame, width=20)
        self.wm_shape_entry.grid(row=1, column=1, pady=5, sticky='w')

        ttk.Label(frame, text="密码:").grid(row=2, column=0, sticky='e', pady=5)
        self.extract_pwd_entry = ttk.Entry(frame, width=20)
        self.extract_pwd_entry.grid(row=2, column=1, pady=5, sticky='w')

        ttk.Button(frame, text="提取水印", command=self._extract_watermark).grid(row=3, column=1, pady=20)

        ttk.Label(frame, text="提取结果:").grid(row=4, column=0, sticky='ne', pady=5)
        self.result_text = tk.Text(frame, height=5, width=40)
        self.result_text.grid(row=4, column=1, columnspan=2, pady=5)

    def _select_original(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if path:
            self.original_path = path
            self.embed_file_label.config(text=path.split('/')[-1])

    def _select_embedded(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if path:
            self.embedded_path = path
            self.extract_file_label.config(text=path.split('/')[-1])

    def _embed_watermark(self):
        if not self.original_path:
            messagebox.showerror("错误", "请先选择原图")
            return
        wm_text = self.wm_text_entry.get()
        if not wm_text:
            messagebox.showerror("错误", "请输入水印文本")
            return
        pwd = self.embed_pwd_entry.get()
        if not pwd:
            messagebox.showerror("错误", "请输入密码")
            return

        out_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")]
        )
        if not out_path:
            return

        try:
            bwm = WaterMark(password_img=int(pwd), password_wm=int(pwd))
            bwm.read_img(self.original_path)
            bwm.read_wm(wm_text, mode='str')
            bwm.embed(out_path)
            wm_len = len(bwm.wm_bit)
            self.embed_info.config(text=f"成功！水印长度: {wm_len} (提取时需要)")
            messagebox.showinfo("成功", f"已生成带水印图片\n水印长度: {wm_len}")
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def _extract_watermark(self):
        if not self.embedded_path:
            messagebox.showerror("错误", "请先选择隐写图片")
            return
        shape_str = self.wm_shape_entry.get()
        if not shape_str:
            messagebox.showerror("错误", "请输入水印长度")
            return
        pwd = self.extract_pwd_entry.get()
        if not pwd:
            messagebox.showerror("错误", "请输入密码")
            return

        try:
            wm_shape = int(shape_str)
            bwm = WaterMark(password_img=int(pwd), password_wm=int(pwd))
            extracted = bwm.extract(self.embedded_path, wm_shape=wm_shape, mode='str')
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, extracted)
        except Exception as e:
            messagebox.showerror("错误", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()
