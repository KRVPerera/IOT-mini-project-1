#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

#include "thread.h"
#include "ztimer.h"

#include "mutex.h"

#include "lpsxxx.h"
#include "lpsxxx_params.h"

#include "msg.h"

#include "net/gcoap.h"
#include "shell.h"
#include "ztimer.h"

static lpsxxx_t lpsxxx;

#define LPSXXX_REG_CTRL_REG2 (0x21)

void temp_sensor_reset(const lpsxxx_t *dev)
{
  if (lpsxxx_init(&lpsxxx, &lpsxxx_params[0]) != LPSXXX_OK)
  {
    puts("sensor init FAILED");
  }
  ztimer_sleep(ZTIMER_MSEC, 3000);
  i2c_acquire(dev->params.i2c);
  if (i2c_write_reg(dev->params.i2c, dev->params.addr, 0x21, 0x44, 0) < 0)
  {
    i2c_release(dev->params.i2c);
    puts("sensor reset FAILED");
  }
  i2c_release(dev->params.i2c);

  ztimer_sleep(ZTIMER_MSEC, 1000);
}


#define MAIN_QUEUE_SIZE (4)
static msg_t _main_msg_queue[MAIN_QUEUE_SIZE];

extern int gcoap_cli_cmd(int argc, char **argv);
extern void gcoap_cli_init(void);

static const shell_command_t shell_commands[] = {
    { "coap", "CoAP example", gcoap_cli_cmd },
    { NULL, NULL, NULL }
};

int main(void)
{

  ztimer_sleep(ZTIMER_MSEC, 3000);
    int coap_command_c = 7;
    char *coap_command[coap_command_c];
    int i;
    i = 0;
    coap_command[i++] = "coap";
    coap_command[i++] = "get";
    // coap_command[i++] = "-c";
    coap_command[i++] = "2600:1f16:15a8:3d9:6df4:e087:ae99:27cc";
    coap_command[i++] = "5683";
    coap_command[i++] = "/.well-known/core";
    // coap_command[5] = "/temp";
    char temp_str[20];  // Allocate memory for the temperature string
    coap_command[i++] = temp_str;

    coap_command_c = i;

        temp_sensor_reset(&lpsxxx);
    msg_init_queue(_main_msg_queue, MAIN_QUEUE_SIZE);
    ztimer_sleep(ZTIMER_MSEC, 1000);

  while (1) {
    
    int16_t temp = 0;
    if (lpsxxx_read_temp(&lpsxxx, &temp) == LPSXXX_OK) {
      sprintf(temp_str, "%d", temp);
      printf("The number as a string is: %s\n", coap_command[coap_command_c-1]);
      // gcoap_post(str, TEMP);
      gcoap_cli_cmd(coap_command_c, coap_command);
    }
    ztimer_sleep(ZTIMER_MSEC, 5000);
  }


  puts("All up, running the shell now");
    char line_buf[SHELL_DEFAULT_BUFSIZE];
    shell_run(shell_commands, line_buf, SHELL_DEFAULT_BUFSIZE);

  return 0;
}
