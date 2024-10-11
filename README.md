# python-ecommerce-project
BTL Python
## Cách dùng git
### Clone repository về máy
1. Clone repository về máy
```bash
git clone https://github.com/PhucLee2304/python-ecommerce-project.git
```
2. Ngay sau khi clone về, tạo một branch mới

```bash
git checkout -b <tên-branch>
```
3. Push branch mới lên github, chỉ cần làm 1 lần - lần đầu tiên
```bash
git push --set-upstream origin <tên-branch>
```
Những lần push code lên github sau, chỉ cần nhập
```bash
git push
```

### Cập nhật branch của mình với những thay đổi của branch main

1. Fetch the latest changes from the remote repository:
```bash
git fetch origin
```
2. Switch to your branch (if you are not already on it):
```bash
git checkout your-branch-name
```
3. Rebase your branch onto the main branch
```bash
git rebase origin/main
```
4. Resolve any conflicts if prompted ( nếu xảy ra lỗi thì giải quyết conflicts r thực hiện 2 lệnh dưới đây, nếu không xảy ra lỗi thì bỏ qua)
```bash
git add .
```
```bash
git rebase --continue
```

Sau dó nếu hiển thị màn hình mà ta không nhập được thì nhập " :wq" -> Enter
5. Push your updated branch to the remote repository
```bash
git push origin your-branch-name
```