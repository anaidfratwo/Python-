import tkinter
import customtkinter
import yt_dlp
from tkinter import filedialog
import threading


def progress_hook(d):
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
        downloaded_bytes = d.get('downloaded_bytes')
        if total_bytes:
            percentage = (downloaded_bytes / total_bytes) * 100
            pPercentage.configure(text=f'{percentage:.2f}%')
            progressBar.set(percentage / 100)
    elif d['status'] == 'finished':
        pPercentage.configure(text='100%')
        progressBar.set(1)



def startDownload():

    ytLink = link.get()  
    save_path = save_path_var.get()  
    if not save_path:
        finishLabel.configure(text="Selectați un folder pentru salvare", text_color="red")
        return

    try:
        with yt_dlp.YoutubeDL() as ydl:
            info_dict = ydl.extract_info(ytLink, download=False)
            video_title = info_dict.get('title', 'Video')  
            title.configure(text=video_title) 
            
        ydl_opts = {
    'format': 'bestvideo+bestaudio[ext=m4a]/best',  
    'outtmpl': f'{save_path}/%(title)s.%(ext)s',  
    'merge_output_format': 'mp4',  
    'ffmpeg_location': 'C:/ffmpeg-7.0.2-full_build/ffmpeg-7.0.2-full_build/bin/ffmpeg.exe',
    'progress_hooks': [progress_hook]  
}
    
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([ytLink])
        print("Download Complete!")
        finishLabel.configure(text = "Downloaded!", text_color="green")
    except Exception as e:
        print(f"Error: {e}")
        print("Linkul YouTube este invalid sau a apărut o problemă la descărcare.")
        finishLabel.configure(text = "Invalid link", text_color="red")


def startDownload_thread():
    threading.Thread(target=startDownload).start()

    
def browse_folder():
    folder_selected = filedialog.askdirectory() 
    if folder_selected:
        save_path_var.set(folder_selected)  



customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("green")


app = customtkinter.CTk()
app.geometry("720x480")
app.title("YouTube Downloader")



title = customtkinter.CTkLabel(app, text="Insert the URL:")
title.pack(padx=10, pady=10)


pPercentage = customtkinter.CTkLabel(app, text="0%")
pPercentage.pack()


progressBar =  customtkinter.CTkProgressBar(app, width=600)
progressBar.set(0)
progressBar.pack(pady=10)



url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable = url_var)
link.pack()


finishLabel =  customtkinter.CTkLabel(app,text = "")
finishLabel.pack()


save_path_var = tkinter.StringVar()
folder_button = customtkinter.CTkButton(app, text="Select Save Location", command=browse_folder)
folder_button.pack(pady=10)




#Download Btn
download = customtkinter.CTkButton(app, text="Download", command=startDownload_thread)
download.pack(pady=20)

#Run app
app.mainloop()