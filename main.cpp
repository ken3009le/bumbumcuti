#include <windows.h>
#include <wrl.h>
#include <WebView2.h>
#include <string>

using namespace Microsoft::WRL;

std::string LoadHtmlFromResource() {
    HRSRC res = FindResource(NULL, MAKEINTRESOURCE(IDR_HTML1), "HTML");
    HGLOBAL data = LoadResource(NULL, res);
    DWORD size = SizeofResource(NULL, res);
    char* ptr = (char*)LockResource(data);
    return std::string(ptr, size);
}

int APIENTRY WinMain(HINSTANCE, HINSTANCE, LPSTR, int) {
    HWND hwnd = CreateWindowA("STATIC", "SPYRONX", WS_OVERLAPPEDWINDOW,
                              CW_USEDEFAULT, CW_USEDEFAULT, 1280, 800,
                              nullptr, nullptr, nullptr, nullptr);

    CreateCoreWebView2EnvironmentWithOptions(nullptr, nullptr, nullptr,
        Callback<ICoreWebView2CreateCoreWebView2EnvironmentCompletedHandler>(
            [hwnd](HRESULT result, ICoreWebView2Environment* env) -> HRESULT {
                env->CreateCoreWebView2Controller(hwnd,
                    Callback<ICoreWebView2CreateCoreWebView2ControllerCompletedHandler>(
                        [hwnd](HRESULT result, ICoreWebView2Controller* controller) -> HRESULT {
                            ComPtr<ICoreWebView2> webview;
                            controller->get_CoreWebView2(&webview);
                            controller->put_IsVisible(TRUE);

                            RECT bounds;
                            GetClientRect(hwnd, &bounds);
                            controller->put_Bounds(bounds);

                            std::string html = LoadHtmlFromResource();
                            std::wstring htmlW(html.begin(), html.end());
                            webview->NavigateToString(htmlW.c_str());

                            return S_OK;
                        }).Get());
                return S_OK;
            }).Get());

    ShowWindow(hwnd, SW_SHOWDEFAULT);
    UpdateWindow(hwnd);

    MSG msg;
    while (GetMessage(&msg, nullptr, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    return 0;
}
