const generateFakeGUID = () => {
    return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function(c) {
        const r = Math.random() * 16 | 0, v = c === "x" ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
};

function generateFakeSHA256() {
    const characters = 'abcdef0123456789';
    let result = '';
    for (let i = 0; i < 64; i++) {
      result += characters[Math.floor(Math.random() * characters.length)];
    }
    return result;
};

const generateFakeDate = () => {
    const start = new Date(2020, 0, 1).getTime();
    const end = new Date().getTime();
  
    const randomTimestamp = Math.floor(Math.random() * (end - start + 1)) + start;
    const date = new Date(randomTimestamp);

    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");
    const hours = String(date.getHours()).padStart(2, "0");
    const minutes = String(date.getMinutes()).padStart(2, "0");
    const seconds = String(date.getSeconds()).padStart(2, "0");

    return `${year}/${month}/${day} ${hours}:${minutes}:${seconds}`;
};

const generateFakeStatus = () => {
    const status = ["Pending", "Analyzing", "Completed", "Failed"];
    const randomIndex = Math.floor(Math.random() * status.length);
    return status[randomIndex];
};

const generateFakeAPICalls = (count: number) => {
    const api_calls = [ 
        "InternetWriteFile", "GlobalMemoryStatus", "CertCreateCertificateContext", "CryptGenKey", "RegCloseKey", "CoCreateInstanceEx", 
        "ShellExecuteExW", "OutputDebugStringA", "HttpSendRequestW", "GetUserNameA", "RegEnumKeyW", "system", "NtCreateFile", 
        "NtUnloadDriver", "NtOpenDirectoryObject", "connect", "RegQueryValueExW", "CertOpenStore", "WriteProcessMemory", 
        "LoadResource", "CreateJobObjectW", "WSASendTo", "CreateThread", "getaddrinfo", "WSASocketA", "NtReadFile", "SetFilePointerEx", 
        "SetWindowsHookExW", "UnhookWindowsHookEx", "DeleteUrlCacheEntryW", "shutdown", "CryptCreateHash", "HttpOpenRequestA", 
        "NtAllocateVirtualMemory", "COleScript_Compile", "NtLoadKey", "RtlAddVectoredContinueHandler", "recvfrom", "GetSystemWindowsDirectoryW", 
        "NtQueryInformationFile", "CryptUnprotectMemory", "CoInitializeSecurity", "NtQueueApcThread", "MessageBoxTimeoutW", "Thread32First", 
        "NtDuplicateObject", "send", "FindWindowA", "InternetQueryOptionA", "gethostbyname", "NtCreateKey", "CreateProcessInternalW", "NtOpenKey", 
        "NtQueryAttributesFile", "RemoveDirectoryW", "CryptDecrypt", "NtProtectVirtualMemory", "__anomaly__", "LdrLoadDll", "SetWindowsHookExA", 
        "NtLoadDriver", "GetKeyboardState", "closesocket", "timeGetTime", "Process32NextW", "OpenServiceA"
    ];

    const result: string[] = [];
    for (let i = 0; i < count; i++) {
        const randomIndex = Math.floor(Math.random() * api_calls.length);
        result.push(api_calls[randomIndex]);
    }
    return result;
};

export const generateFakeData = () => {
    const id = generateFakeGUID();
    const status = generateFakeStatus();
    return {
      id: id,
      name: `test_file_${id.split("-")[0]}.exe`,
      SHA256: generateFakeSHA256(),
      uploadTime: generateFakeDate(),
      analysisStart: status === "Pending" ? "N/A" : generateFakeDate(),
      analysisCompleted: status === "Completed" ? generateFakeDate() : "N/A",
      status: status,
      result: status === "Completed" ? Math.floor(Math.random() * 2) : -1,
      apiCalls: status === "Completed" ? generateFakeAPICalls(100) : ["N/A"]
    };
};

export const generateFakeDataSource = (count: number) => {
    const data = [];
    for (let i = 1; i <= count; i++) {
      const item = generateFakeData();
      data.push({
        number: i,
        ...item
      });
    }
    return data;
};