// LED status updates
//
// Copyright (C) 2021 Eric Callahan <arksine.code@gmail.com>
//
// This file may be distributed under the terms of the GNU GPLv3 license.

#include "autoconf.h" // CONFIG_ENABLE_LED
#include "board/gpio.h" // gpio_out_setup
#include "board/misc.h" // timer_read_time
#include "ctr.h" // DECL_CTR
#include "flashcmd.h" // flashcmd_is_in_transfer
#include "sched.h" // DECL_INIT

#define WAIT_BLINK_TIME 1000000
#define XFER_BLINK_TIME 20000

DECL_CTR("DECL_LED_PIN " __stringify(CONFIG_STATUS_LED_PIN));
extern uint32_t led_gpio, led_gpio_high; // Generated by buildcommands.py

static struct gpio_out led;
static uint32_t last_blink_time;

void
led_init(void)
{
    led = gpio_out_setup(led_gpio, led_gpio_high);
    last_blink_time = timer_read_time();
}
DECL_INIT(led_init);

void
led_blink_task(void)
{
    int in_transfer = flashcmd_is_in_transfer();
    uint32_t usec = in_transfer ? XFER_BLINK_TIME : WAIT_BLINK_TIME;
    uint32_t curtime = timer_read_time();
    uint32_t endtime = last_blink_time + timer_from_us(usec);
    if (timer_is_before(endtime, curtime)) {
        gpio_out_toggle(led);
        last_blink_time = timer_read_time();
    }
}
DECL_TASK(led_blink_task);