# Build interfaces

计划提供稳定入口：

```text
make bootstrap
make audit-rootfs
make kernel
make packages
make image
make validate
make manifest
make test-image
```

所有接口都必须接受显式 manifest 路径，并拒绝浮动、缺失完整性信息或同名覆盖的
release。实现前不提供会误导用户的空命令。
