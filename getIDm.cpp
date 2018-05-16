#include <stdio.h>
#include <string>
#include "RCS620S.h"

int main()
{
    RCS620S rcs620s;
    
    int ret = rcs620s.initDevice();
    if (!ret)
    {
        printf("can't open pasori\n");
        return 0;
    }
    
    char s[256] = {'\0'};
    do
    {
        ret = rcs620s.polling();
        
        if (ret)
        {
            uint8_t *idm = rcs620s.idm;
            sprintf(s, "%02x:%02x:%02x:%02x:%02x:%02x:%02x:%02x\n",
                    idm[0], idm[1], idm[2], idm[3],
                    idm[4], idm[5], idm[6], idm[7]);
        }
    } while (printf(s) == 0);
    printf("%02x", s);
    
    rcs620s.rfOff();
    
    return 0;
}
