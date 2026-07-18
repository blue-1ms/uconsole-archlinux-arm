# Image composition

Image composer 将在 Linux VM 的 guest-local filesystem 中完成 rootfs 解包、
package 安装、boot tree 生成和验证。只在所有检查通过后导出普通 image file。

约束：

- host 不直接在共享目录内编译 kernel/package；
- 不写真实 SD 卡或其他物理 disk；
- rootfs 和 package 输入必须离线、签名且 manifest-pinned；
- 保留 Mac 可读 FAT boot 分区；
- image 内不保留 build tree、package cache、machine-id、host keys、默认密码或
  用户认证状态；
- 导出前执行只读 mounted-image validation。
