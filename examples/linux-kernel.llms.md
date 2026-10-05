# Linux kernel

> The core of any Linux operating system that manages hardware, system resources, and provides fundamental services for all other software.

It is built using the Kbuild system and documented in the Documentation directory. The documentation covers building requirements, coding style, subsystem internals, security, and specific guides for developers, maintainers, and AI assistants.

## Docs

- [Linux kernel](https://raw.githubusercontent.com/torvalds/linux/master/README): Kernel overview, quick start links, essential documentation, and role-based guides for developers, researchers, and administrators.
- [Kernel subsystem documentation](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/subsystem-apis.rst): Detailed developer guides for core, human interface, networking, storage, and other specific kernel subsystems.
- [The Linux Kernel documentation](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/index.rst): Top-level documentation tree covering development community guides, internal API manuals, tools, and user-oriented documentation.

## Guides

- [Working with the kernel development community](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/process/index.rst): Guides on development process, patch submission, coding style, tools, and community policies for kernel developers.
- [Kernel Maintainer Handbook](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/maintainer/index.rst): Manual for kernel maintainers covering git configuration, rebasing, merging, pull requests, and patch modification.
- [Core API Documentation](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/core-api/index.rst): Manuals for core kernel APIs, data structures, concurrency primitives, and low-level hardware management utilities.
- [Driver implementer's API guide](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/driver-api/index.rst): Driver basics, support libraries, bus-level documentation, and subsystem-specific APIs for device driver development.
- [Locking](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/locking/index.rst): Lock types, lockdep design, lockstat, locktorture, mutex, rt-mutex, seqlock, spinlocks, and futex documentation.
- [Kernel tools](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/tools/index.rst): User-space tools shipped with the kernel source, including rtla, rv, python, and sbom.
- [How to write kernel documentation](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/doc-guide/index.rst): Sphinx, kernel-doc, header parsing, contributing guidelines, maintainer profiles, and translation update checks.
- [Development tools for the kernel](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/dev-tools/index.rst): Testing, static analysis, sanitizers, and other development tools for working on the Linux kernel.
- [Kernel Hacking Guides](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/kernel-hacking/index.rst): Hacking guides, locking documentation, and false sharing information for kernel developers.
- [Linux Tracing Technologies Guide](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/trace/index.rst): Overview of tracing frameworks, event analysis, hardware performance monitoring, user-space tools, and remote tracing.
- [Fault-injection](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/fault-injection/index.rst): Documentation for fault injection, notifier error injection, NVMe fault injection, and crash provocation mechanisms.
- [Kernel Livepatching](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/livepatch/index.rst): Documentation covering livepatching, callbacks, cumulative patches, module formats, shadow variables, and system state management.
- [Rust](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/rust/index.rst): Rust kernel documentation, including quick-start guides, coding guidelines, architecture support, testing, and generated code documentation.
- [The Linux kernel user's and administrator's guide](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/admin-guide/index.rst): User and administrator guides covering kernel parameters, virtual filesystems, security, booting, and problem tracking.
- [Kernel Build System](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/kbuild/index.rst): Documentation for the kernel build system, including Kconfig, makefiles, modules, headers, and reproducible builds.
- [The Linux kernel user-space API guide](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/userspace-api/index.rst): System calls, security interfaces, device I/O, and miscellaneous user-space API documentation.
- [The Linux kernel firmware guide](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/firmware-guide/index.rst): ACPI subsystem description from a firmware perspective.
- [Open Firmware and Devicetree](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/devicetree/index.rst): Kernel Devicetree usage, overlays, and bindings documentation.
- [CPU Architectures](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/arch/index.rst): Architecture-specific programming details for various CPU architectures.
- [Unsorted Documentation](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/staging/index.rst): Unsorted documentation covering CRC32, LZO, remoteproc, and other miscellaneous topics.

## Optional

- [PCI Bus Subsystem](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/PCI/index.rst): PCI bus subsystem documentation, including PCIe, MSI, error recovery, and endpoints.
- [RCU Handbook](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/RCU/index.rst): RCU design, memory ordering, grace periods, data structures, and requirements.
- [Compute Accelerators](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/accel/index.rst): Introduction to compute accelerators, including AMD XDNA, Qaic, and Rocket drivers.
- [Accounting](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/accounting/index.rst): Cgroup statistics, delay accounting, pressure stall information, and task statistics.
- [Block](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/block/index.rst): Block layer I/O schedulers, multi-queue, data integrity, encryption, and error injection.
- [BPF Documentation](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/bpf/index.rst): EBPF verifier, libbpf, standardization, BTF, syscalls, helpers, programs, and maps.
- [A Linux CD-ROM standard](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/cdrom/cdrom-standard.rst): Standardization of CD-ROM device driver behavior and ioctl calls across Linux hardware.
- [CPUFreq - CPU frequency and voltage scaling code in the Linux(TM) kernel](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/cpu-freq/index.rst): CPU frequency and voltage scaling concepts, mailing list details, and links to FTP archives and driver projects.
- [Crypto API](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/crypto/index.rst): Linux kernel crypto API concepts, cipher implementation development, cryptographic use cases, and programming examples.
- [EDAC Subsystem](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/edac/index.rst): Documentation for EDAC subsystem features, memory repair mechanisms, and scrubbing operations.
- [Frame Buffer](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/fb/index.rst): Frame buffer API, internals, and driver documentation for various hardware framebuffer implementations.
- [Filesystems in the Linux kernel](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/filesystems/index.rst): Linux virtual filesystem layer documentation, support layers, and implementations for numerous filesystem types.
- [FPGA Device Feature List (DFL) Framework Overview](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/fpga/dfl.rst): FPGA Device Feature List framework overview, unified userspace interfaces, and feature enumeration mechanisms.
- [GPU Driver Developer's Guide](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/gpu/index.rst): Index of GPU driver documentation covering DRM internals, memory management, KMS, RAS, UAPI, and client interfaces.
- [Human Interface Devices (HID)](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/hid/index.rst): Index of HID documentation covering introductions, hiddev, hidraw, sensors, transports, BPF, and vendor-specific drivers.
- [Hardware Monitoring](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/hwmon/index.rst): Index of hardware monitoring documentation covering kernel APIs, PMBus, sysfs interfaces, userspace tools, and driver lists.
- [I2C/SMBus Subsystem](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/i2c/index.rst): Index of I2C/SMBus documentation covering protocols, device instantiation, driver writing, debugging, slave interfaces, and advanced topics.
- [Industrial I/O](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/iio/index.rst): Index of Industrial I/O documentation covering ADCs, configfs, devbuf, dmabuf APIs, tools, and kernel driver lists.
- [InfiniBand](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/infiniband/index.rst): Index of InfiniBand documentation covering core locking, ipoib, sysfs, tag matching, user MAD, and user verbs.
- [Input Documentation](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/input/index.rst): Index for input subsystem documentation, covering user-space API, kernel API, and device drivers.
- [LEDs](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/leds/index.rst): Documentation for LED classes, triggers, and specific hardware drivers like blinkm and lp55xx.
- [MHI (Modem Host Interface)](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/mhi/mhi.rst): Overview of the MHI protocol, its internals, MMIO registers, and logical channel management.
- [Assorted Miscellaneous Devices Documentation](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/misc-devices/index.rst): Documentation for miscellaneous devices that do not fit into other standard kernel categories.
- [Memory Management Documentation](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/mm/index.rst): Guide to Linux memory management internals, including page tables, allocation, swap, and OOM handling.
- [NetLabel](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/netlabel/index.rst): Documentation for NetLabel, covering introduction, CIPSO IPv4, and the LSM interface.
- [Netlink Family Specifications](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/netlink/specs/index.rst): Index of Netlink family specifications.
- [Networking](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/networking/index.rst): Index of networking documentation covering protocols, drivers, and subsystems.
- [LIBNVDIMM Maintainer Entry Profile](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/nvdimm/maintainer-entry-profile.rst): Submission guidelines, mailing list details, and testing requirements for the libnvdimm subsystem.
- [NVMe Subsystem](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/nvme/index.rst): Index of NVMe subsystem documentation, including feature policies and endpoint targets.
- [PCMCIA](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/pcmcia/index.rst): Index of PCMCIA documentation covering drivers, device tables, and locking.
- [Peci](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/peci/peci.rst): Overview of the PECI interface, wire protocol, and communication between processors and management controllers.
- [Power Management](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/power/index.rst): Index of power management topics including suspend, runtime PM, regulators, and power supply classes.
- [Scheduler](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/scheduler/index.rst): Index of scheduler documentation covering CFS, EEVDF, deadline, real-time, and extended scheduler interfaces.
- [SCSI Subsystem](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/scsi/index.rst): Index of SCSI subsystem documentation including driver APIs, parameters, and host adapter drivers.
- [Security Documentation](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/security/index.rst): Index of security documentation covering credentials, LSMs, IMA, TPM, Landlock, and secrets management.
- [Sound Subsystem Documentation](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/sound/index.rst): Index of sound subsystem documentation including kernel APIs, designs, ALSA configuration, and codecs.
- [Indices](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/sphinx-includes/subproject-index.rst): General index of all terms and topics across the Linux kernel documentation.
- [Serial Peripheral Interface (SPI)](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/spi/index.rst): SPI overview, device instantiation, spidev, multiple data lanes, butterfly, and specific controller documentation.
- [TCM Virtual Device](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/target/index.rst): TCM virtual device design, module builder, and associated scripts for target core module.
- [TEE Subsystem](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/tee/index.rst): TEE subsystem overview, OP-TEE, AMD TEE, TrustZone TEE, and Qualcomm TEE implementation details.
- [Timers](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/timers/index.rst): High-resolution timers, HPET, hrtimers, no-hz idle, timekeeping, and delay sleep function documentation.
- [USB support](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/usb/index.rst): USB host controllers, gadget drivers, mass storage, USBIP protocol, monitoring, and serial support.
- [Virtualization Support](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/virt/index.rst): KVM, User-Mode Linux, paravirtualization, guest halt polling, ACRN, SEV, TDX, and Hyper-V support.
- [1-Wire Subsystem](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/w1/index.rst): Index for generic 1-Wire drivers, netlink interface, master controllers, and slave devices.
- [Watchdog Support](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/watchdog/index.rst): Kernel watchdog infrastructure APIs, power management, driver conversion guides, and specific driver documentation.
- [WMI Subsystem](https://raw.githubusercontent.com/torvalds/linux/master/Documentation/wmi/index.rst): WMI subsystem documentation covering ACPI interface, driver development guide, and supported device list.
