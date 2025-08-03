package main

import (
	"embed"
	"io/fs"
	"net/http"
	"github.com/webview/webview"
)

//go:embed index.html media2.json icon.ico
var content embed.FS

func main() {
	// Tạo HTTP FS server nội bộ
	fsys, _ := fs.Sub(content, ".")
	go func() {
		http.Handle("/", http.FileServer(http.FS(fsys)))
		http.ListenAndServe("127.0.0.1:8080", nil)
	}()

	// Mở WebView trình duyệt offline
	webview.Open("Tài Liệu Mật", "file://"+filepath.Join(dir, "index.html"), 1280, 800, true)

}
