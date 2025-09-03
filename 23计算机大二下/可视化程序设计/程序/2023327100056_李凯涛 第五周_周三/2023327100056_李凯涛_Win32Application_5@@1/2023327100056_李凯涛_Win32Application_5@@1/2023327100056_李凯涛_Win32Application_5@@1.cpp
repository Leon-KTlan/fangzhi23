
#include "framework.h"
#include "2023327100056_李凯涛_Win32Application_5@@1.h"

#define MAX_LOADSTRING 100

// 全局变量:
HINSTANCE hInst;                                // 当前实例
WCHAR szTitle[MAX_LOADSTRING];                  // 标题栏文本
WCHAR szWindowClass[MAX_LOADSTRING];            // 主窗口类名
POINT startPoint;       // 鼠标按下时的起始点
RECT currentRect;       // 当前绘制的矩形区域
BOOL isDrawing = FALSE; // 是否正在绘制矩形
BOOL isStretching = FALSE; // 是否正在拉伸矩形

// 此代码模块中包含的函数的前向声明:
ATOM                MyRegisterClass(HINSTANCE hInstance);
BOOL                InitInstance(HINSTANCE, int);
LRESULT CALLBACK    WndProc(HWND, UINT, WPARAM, LPARAM);
INT_PTR CALLBACK    About(HWND, UINT, WPARAM, LPARAM);

int APIENTRY wWinMain(_In_ HINSTANCE hInstance,
    _In_opt_ HINSTANCE hPrevInstance,
    _In_ LPWSTR    lpCmdLine,
    _In_ int       nCmdShow)
{
    UNREFERENCED_PARAMETER(hPrevInstance);
    UNREFERENCED_PARAMETER(lpCmdLine);

    // 初始化全局字符串
    LoadStringW(hInstance, IDS_APP_TITLE, szTitle, MAX_LOADSTRING);
    LoadStringW(hInstance, IDC_MY2023327100056WIN32APPLICATION51, szWindowClass, MAX_LOADSTRING);
    MyRegisterClass(hInstance);

    // 执行应用程序初始化:
    if (!InitInstance(hInstance, nCmdShow))
    {
        return FALSE;
    }

    HACCEL hAccelTable = LoadAccelerators(hInstance, MAKEINTRESOURCE(IDC_MY2023327100056WIN32APPLICATION51));

    MSG msg;

    // 主消息循环:
    while (GetMessage(&msg, nullptr, 0, 0))
    {
        if (!TranslateAccelerator(msg.hwnd, hAccelTable, &msg))
        {
            TranslateMessage(&msg);
            DispatchMessage(&msg);
        }
    }

    return (int)msg.wParam;
}

//
//  函数: MyRegisterClass()
//
//  目标: 注册窗口类。
//
ATOM MyRegisterClass(HINSTANCE hInstance)
{
    WNDCLASSEXW wcex;

    wcex.cbSize = sizeof(WNDCLASSEX);

    wcex.style = CS_HREDRAW | CS_VREDRAW;
    wcex.lpfnWndProc = WndProc;
    wcex.cbClsExtra = 0;
    wcex.cbWndExtra = 0;
    wcex.hInstance = hInstance;
    wcex.hIcon = LoadIcon(hInstance, MAKEINTRESOURCE(IDI_MY2023327100056WIN32APPLICATION51));
    wcex.hCursor = LoadCursor(hInstance, MAKEINTRESOURCE(IDC_POINTER));
    wcex.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);
    wcex.lpszMenuName = MAKEINTRESOURCEW(IDC_MY2023327100056WIN32APPLICATION51);
    wcex.lpszClassName = szWindowClass;
    wcex.hIconSm = LoadIcon(wcex.hInstance, MAKEINTRESOURCE(IDI_SMALL));

    return RegisterClassExW(&wcex);
}

//
//   函数: InitInstance(HINSTANCE, int)
//
//   目标: 保存实例句柄并创建主窗口
//
BOOL InitInstance(HINSTANCE hInstance, int nCmdShow)
{
    hInst = hInstance; // 将实例句柄存储在全局变量中

    HWND hWnd = CreateWindowW(szWindowClass, szTitle, WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, 0, CW_USEDEFAULT, 0, nullptr, nullptr, hInstance, nullptr);

    if (!hWnd)
    {
        return FALSE;
    }

    ShowWindow(hWnd, nCmdShow);
    UpdateWindow(hWnd);

    return TRUE;
}

//
//  函数: WndProc(HWND, UINT, WPARAM, LPARAM)
//
//  目标: 处理主窗口的消息。
//
LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam)
{
    switch (message)
    {
    case WM_COMMAND:
    {
        int wmId = LOWORD(wParam);
        switch (wmId)
        {
        case IDM_ABOUT:
            DialogBox(hInst, MAKEINTRESOURCE(IDD_ABOUTBOX), hWnd, About);
            break;
        case IDM_EXIT:
            DestroyWindow(hWnd);
            break;
        default:
            return DefWindowProc(hWnd, message, wParam, lParam);
        }
    }
    break;

    case WM_LBUTTONDOWN:
    {
        startPoint.x = LOWORD(lParam);
        startPoint.y = HIWORD(lParam);
        isDrawing = TRUE;
        SetCursor(LoadCursor(nullptr, IDC_CROSS)); // 设置为十字型光标
    }
    break;

    case WM_MOUSEMOVE:
    {
        if (isDrawing)
        {
            POINT currentPoint;
            currentPoint.x = LOWORD(lParam);
            currentPoint.y = HIWORD(lParam);
            currentRect.left = min(startPoint.x, currentPoint.x);
            currentRect.top = min(startPoint.y, currentPoint.y);
            currentRect.right = max(startPoint.x, currentPoint.x);
            currentRect.bottom = max(startPoint.y, currentPoint.y);
            InvalidateRect(hWnd, nullptr, TRUE); // 重绘窗口
            SetCursor(LoadCursor(nullptr, IDC_CROSS)); // 保持十字型光标
        }
    }
    break;

    case WM_LBUTTONUP:
    {
        if (isDrawing)
        {
            isDrawing = FALSE;
            isStretching = TRUE;
            SetCursor(LoadCursor(nullptr, IDC_WAIT)); // 设置为沙漏型光标

            // 立即拉伸到整个窗口
            GetClientRect(hWnd, &currentRect);
            InvalidateRect(hWnd, nullptr, TRUE); // 重绘窗口
            isStretching = FALSE;
            SetCursor(LoadCursor(nullptr, IDC_ARROW)); // 恢复默认光标
        }
    }
    break;

    case WM_LBUTTONDBLCLK:
    {
        isDrawing = FALSE;
        isStretching = FALSE;
        InvalidateRect(hWnd, nullptr, TRUE); // 重绘窗口，清除灰色矩形
    }
    break;

    case WM_PAINT:
    {
        PAINTSTRUCT ps;
        HDC hdc = BeginPaint(hWnd, &ps);

        if (isDrawing || isStretching)
        {
            // 绘制灰色矩形
            HBRUSH hBrush = CreateSolidBrush(RGB(128, 128, 128)); // 灰色
            FillRect(hdc, &currentRect, hBrush);
            DeleteObject(hBrush);
        }
        else
        {
            // 绘制初始状态的“涛”字
            SetTextColor(hdc, RGB(255, 0, 0)); // 红色字体
            SetBkColor(hdc, RGB(255, 255, 0)); // 黄色背景
            TextOutW(hdc, 10, 10, L"涛", 1);
        }

        EndPaint(hWnd, &ps);
    }
    break;

    case WM_DESTROY:
        PostQuitMessage(0);
        break;

    default:
        return DefWindowProc(hWnd, message, wParam, lParam);
    }
    return 0;
}

// “关于”框的消息处理程序。
INT_PTR CALLBACK About(HWND hDlg, UINT message, WPARAM wParam, LPARAM lParam)
{
    UNREFERENCED_PARAMETER(lParam);
    switch (message)
    {
    case WM_INITDIALOG:
        return (INT_PTR)TRUE;

    case WM_COMMAND:
        if (LOWORD(wParam) == IDOK || LOWORD(wParam) == IDCANCEL)
        {
            EndDialog(hDlg, LOWORD(wParam));
            return (INT_PTR)TRUE;
        }
        break;
    }
    return (INT_PTR)FALSE;
}