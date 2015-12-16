#include <stdio.h>

#include <sys/mman.h>
#include <sys/types.h>
#include <sys/stat.h>

#include <unistd.h>

// Define which Raspberry Pi board are you using. Take care to have defined only one at time.
//#define RPI
#define RPI2

#ifdef RPI
#define BCM2708_PERI_BASE       0x20000000
#define GPIO_BASE               (BCM2708_PERI_BASE + 0x200000)  // GPIO controller
#define BSC0_BASE               (BCM2708_PERI_BASE + 0x205000)  // I2C controller
#endif

#ifdef RPI2
#define BCM2708_PERI_BASE       0x3F000000
#define GPIO_BASE               (BCM2708_PERI_BASE + 0x200000)  // GPIO controller. Maybe wrong. Need to be tested.
#define BSC0_BASE               (BCM2708_PERI_BASE + 0x804000)  // I2C controller
#endif

#define BLOCK_SIZE 		(4 * 1024)

#define INP_GPIO(g)		*(gpio.addr + ((g)/10)) &= ~(7<<(((g)%10)*3))
#define OUT_GPIO(g)		*(gpio.addr + ((g)/10)) |=  (1<<(((g)%10)*3))
#define SET_GPIO_ALT(g,a)	*(gpio.addr + ((g)/10)) |= (((a)<=3? (a)+4:(a)==4? 3:2) << (((g)%10)*3))

#define GPIO_SET 		*(gpio.addr + 7)
#define GPIO_CLR		*(gpio.addr + 10)

#define GPIO_READ(g)		*(gpio.addr + 13) &= (1<<(g))

// IO Access
struct bcm2835_peripheral {
	unsigned long addr_p;
	int mem_fd;
	void *map;
	volatile unsigned int *addr;
};

extern struct bcm2835_peripheral gpio;
extern int map_peripheral(struct bcm2835_peripheral *);

