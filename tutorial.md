# Qemu and Linux kernel hacking

We are going to compile Qemu (emulator) from source so we can modify it in an other tutorial.
We will add a custom system call in the linux, compile the linux kernel, and finally write program to call our syscall (ramfs are usually used to start the actual system but we are going to write our own minimalist system).

Objective: Get more familiar with the linux kernel environment/structure.

## Setting up Qemu
- Download QEmu:
```
wget https://download.qemu.org/qemu-5.1.0.tar.xz
```
- Untar/Uncompress (keep the archive so you can revert your changes if needed):
```
tar xf ./qemu-5.1.0.tar.xz && cd
qemu-5.1.0
```
- Create a directory for your experimental Qemu: 
```
mkdir ../qemu_bin
```
- Check for dependencies for your platform https://wiki.qemu.org/Hosts/Linux 
- If you are on debian you can use:
```
sudo apt-get install git
	   libglib2.0-dev libfdt-dev
	   libpixman-1-dev
	   zlib1g-dev
```
- Configure: 
```
./configure --prefix=$PWD/../qemu_bin
```
- Make: 
```
make
```
Note: you can have a look at the next section while this is running
- Install (in your test directory): 
```
make install
```
## Getting a Linux image
If you want to learn more about creating your own embedded linux: https://wiki.gentoo.org/wiki/Custom_Initramfs | https://tldp.org/HOWTO/Bootdisk-HOWTO/x88.html | https://tldp.org/HOWTO/From-PowerUp-To-Bash-Prompt-HOWTO.html | https://www.linuxfromscratch.org/lfs/view/stable/
- Get linux source code
- Start with a default linux kernel config:
```
make defconfig # Get default config

# Make sure you have the following settings in .config
CONFIG_EXT4_FS=y
CONFIG_IA32_EMULATION=y
CONFIG_VIRTIO_PCI=y (Virtualization -> PCI driver for virtio devices)
CONFIG_VIRTIO_BALLOON=y (Virtualization -> Virtio balloon driver)
CONFIG_VIRTIO_BLK=y (Device Drivers -> Block -> Virtio block driver)
CONFIG_VIRTIO_NET=y (Device Drivers -> Network device support -> Virtio network
driver)
CONFIG_VIRTIO=y
CONFIG_VIRTIO_RING=y

```
- You can edit your config with the nice ncurse interface: 
```
make menuconfig
```
- Optional: Make an image to be used inside Qemu: (Will take a while)
```
make bzImage
```
- Optional: Create an initial system to run:
```
/sbin/mkinitramfs -o ramdisk.img
```
- Optional: Try your kernel:
```
# To quit: Ctrl+a c q
./bin/qemu-system-x86_64 -drive driver=raw,file=./hd.img,if=virtio \
	-m 1024 \
	-kernel /data/projects/linux_staging/arch/x86/boot/bzImage \
	-initrd ramdisk.img \
	-no-reboot \
	-nographic -append "console=ttyS0"
```
- Optional: If you want to graphical interface:
```
cd your_path_to_qemu_bin/
# Create a virtual hard-drive
./bin/qemu-img create -f raw hd.img 8G
./bin/qemu-system-x86_64 -drive driver=raw,file=./hd.img,if=virtio \
	-m 1024 \
	-kernel /data/projects/linux_staging/arch/x86/boot/bzImage \
	-initrd ramdisk.img \
	-no-reboot

```
Install a vnc client (example for debian):

```
sudo apt install tigervnc-viewer
```

Get the screen from your Qemu VM:

```
vncviewer
127.0.0.1::5900
```
## Add a syscall in the linux kernel
- arch/x86/entry/syscalls/syscall_64.tbl
```
# After the last common entry
447	common	hello	sys_hello

```
- kernel/sys.c
```
struct __attribute__((__packed__)) filestat {
	unsigned long st_dev; /* ID of device containing file */
	unsigned long st_uid; /* user ID of owner */
	unsigned long st_gid; /* group ID of owner */
	unsigned long st_rdev; /* device ID (if special file) */
};

SYSCALL_DEFINE2(hello, const char*, path, struct filestat*, buf)
{
	char buffer[256];
	long copied = strncpy_from_user(buffer, path, sizeof(buffer));
	if (copied < 0 || copied == sizeof(buffer))
	return -EFAULT;
	printk(KERN_INFO "hello argument from the user: \"%s\"\n",
	buf->st_dev = 42; // Just a simple test
	return 0;
}

```
## Write a C program calling this syscall
You can learn more about syscall by reading the
manual: 
```
man –S 2 intro
```
- test.c
```
#include <stdio.h>
#include <stdio.h>
#include <unistd.h>

struct __attribute__((__packed__)) filestat {
	unsigned long st_dev; /* ID of device containing file */
	unsigned long st_uid; /* user ID of owner */
	unsigned long st_gid; /* group ID of owner */
	unsigned long st_rdev; /* device ID (if special file) */
};

int main(int argc, char* argv[])
{
	printf("Testing syscall 447...\n");
	char array[] = "Hello, world!\n";
	struct filestat fs;
	fs.st_dev = 0;
	printf("st_dev before call %ld.\n", fs.st_dev);
	long res = syscall(447, array, &fs);
	printf("System call returned %ld.\n", res);
	printf("st_dev after call %ld.\n", fs.st_dev);
	sleep(999999999);
}

```
- Compile (Statically): 
```
gcc -static test.c -o init
```
- Convert to RAM filesystem: 
```
echo init | cpio -o -H newc | gzip > test.cpio.gz
```
- Run (Ctrl+a c q to quit):
```
./bin/qemu-system-x86_64 -drive driver=raw,file=./hd.img,if=virtio \
-m 1024 \
-kernel /data/projects/linux_staging/arch/x86/boot/bzImage \
-initrd ./test.cpio.gz \
-no-reboot \
-nographic -append "console=ttyS0"
```
## Write a syscall that does something
By the time you read this I am very likely done with writing it, just ping me so I update it

## Add instruction in Qemu

You can learn more about Qemu insternals here: https://qemu.weilnetz.de/w32/2011/2011-10-28/qemu-tech.html 

### CPUID
The CPUID instruction is used by software (on Intel CPU) to learn about the details of the processor.
Learn more on wikipedia: https://en.wikipedia.org/wiki/CPUID . This mechanism enable the software to check for accelerated hardware...

We will add an entry to CPUID, when called it should set the bit 10 of RDX.

 - Write a simple C program calling the cpuid instruction and checking the features: cpuid.c
```
#include <stdio.h>

int main(int argc, char** argv) {
	unsigned int rax, rbx, rcx, rdx;
	puts("Calling cpuid");
	__asm__ __volatile__ ("movq $1, %%rax\n\t"
			"cpuid"
			:
			"=a"(rax),
			"=b"(rbx),
			"=c"(rcx),
			"=d"(rdx));
	printf("rdx = %x\n", rdx);
	if (rdx & (1 << 10)) {
		puts("[v] Hello feature OK");
	}
	else
	{
		puts("[x] Hello feature MISSING");
	}
	return 0;
}
```
 - Have a look at what CPUID returns before you make any modification to Qemu (using the nice qemu user space emulation)
```
gcc cpuid.c -o cpuid
../qemu_bin/bin/qemu-x86_64 ./cpuid # qemu_i386 if your gcc is 32 bits
# Should return: Hello feature missing
```
 - Edit Qemu: Add which bit of CPUID you want to set in (In the example HELLO feature at bit 10) target/i386/cpu.h
```
/* cpuid_features bits */
#define CPUID_FP87 (1U << 0)
#define CPUID_VME  (1U << 1)
#define CPUID_DE   (1U << 2)
#define CPUID_PSE  (1U << 3)
#define CPUID_TSC  (1U << 4)
#define CPUID_MSR  (1U << 5)
#define CPUID_PAE  (1U << 6)
#define CPUID_MCE  (1U << 7)
#define CPUID_CX8  (1U << 8)
#define CPUID_APIC (1U << 9)
#define CPUID_HELLO (1U << 10) // <= Add this
#define CPUID_SEP  (1U << 11)
#define CPUID_MTRR (1U << 12)
#define CPUID_PGE  (1U << 13)
#define CPUID_MCA  (1U << 14)
#define CPUID_CMOV (1U << 15)
#define CPUID_PAT  (1U << 16)
#define CPUID_PSE36   (1U << 17)
#define CPUID_PN   (1U << 18)
#define CPUID_CLFLUSH (1U << 19)
#define CPUID_DTS (1U << 21)
#define CPUID_ACPI (1U << 22)
#define CPUID_MMX  (1U << 23)
#define CPUID_FXSR (1U << 24)
#define CPUID_SSE  (1U << 25)
#define CPUID_SSE2 (1U << 26)
#define CPUID_SS (1U << 27)
#define CPUID_HT (1U << 28)
#define CPUID_TM (1U << 29)
#define CPUID_IA64 (1U << 30)
#define CPUID_PBE (1U << 31)
```
 - Add line 736 of file target/i386/cpu.c a clear text name for your feature
```
static FeatureWordInfo feature_word_info[FEATURE_WORDS] = {
	[FEAT_1_EDX] = {
		.type = CPUID_FEATURE_WORD,
		.feat_names = {
				...
			"cx8", "apic", "hello", "sep", // Hello should be the 10th item
				...
```
 - If you want to add your feature to Pentium: edit target/i386/cpu.c line 620 (or PPRO_FEATURES which qemu_32 and 64 uses)
```
#define PENTIUM_FEATURES (I486_FEATURES | CPUID_DE | CPUID_TSC | \
	CPUID_MSR | CPUID_MCE | CPUID_CX8 | CPUID_MMX | CPUID_APIC | CPUID_HELLO)
```
 - Compile and run in Qemu
```
make # compile Qemu
make install # install qemu in your experiment directory (../qemu_bin)
../qemu_bin/bin/qemu-x86_64 ./cpuid # qemu_i386 if your gcc is 32 bits
# Should return: Hello feature OK
```

### Opcode 0xF1

We'll now change the behavior of opcode 0xF1 (In Circuit Emulator BreakPoint) to something else.

## Create performance monitoring linux kernel module

## Create a page fault profiler linux kernel module

## Write a multi-threading library

## Write your own CPU simulator using Qemu

## Add GCC support for your own CPU

## Further reading
Understanding the Linux Kernel, Third Edition by Daniel P. Bovet, Marco Cesati Ph.D
