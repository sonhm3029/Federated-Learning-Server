# Federated learning server with gRPC

## Core module

- Server
- ClientProxy
- ClientManager
- GrpcBridge
- Strategy

## Merge repo khac vào repo đã có giữ nguyên history

- Bước 1: Clone project Demo_v1_ISOFH từ GitLab:

```cmd
git clone <url_to_Demo_v1_ISOFH_repository>
cd Demo_v1_ISOFH
```

- Bước 2: Thêm remote repository của project grpc:

```cmd
git remote add grpc <url_to_grpc_repository>

```

- Bước 3: Merge project grpc vào trong dự án Demo_v1_ISOFH:

```cmd
git fetch grpc
git merge grpc/master --allow-unrelated-histories

```

Lưu ý rằng --allow-unrelated-histories được sử dụng để cho phép hợp nhất lịch sử không liên quan từ hai repository khác nhau.

- Bước 4: Giải quyết xung đột (nếu có):

Khi bạn merge hai dự án có lịch sử không liên quan, xung đột có thể xảy ra. Bạn cần giải quyết xung đột này bằng cách chọn những thay đổi bạn muốn giữ lại và loại bỏ những thay đổi không cần thiết.

- Bước 5: Commit và push thay đổi:

```cmd
git commit -m "Merge grpc project into Demo_v1_ISOFH"
git push origin master

```
