#include "HardwareSerial.h"

HardwareSerial::HardwareSerial()
{
    this->serialFd = serialOpen("/dev/ttyAMA0",115200);
}

HardwareSerial::~HardwareSerial()
{
    if(this->serialFd<0) return;

    serialClose(this->serialFd);
}

void HardwareSerial::write(const uint8_t* data, uint16_t len)
{
    if(this->serialFd<0) return;

    for(uint16_t i=0;i<len;i++)
    {
        serialPutchar(this->serialFd, data[i]);
    }
}

uint8_t HardwareSerial::read()
{
    if(this->serialFd<0) return 0;

    return serialGetchar(this->serialFd);
}

bool HardwareSerial::available()
{
    if(this->serialFd<0) return false;

    return serialDataAvail(this->serialFd) > 0;
}

void HardwareSerial::flush()
{
    if(this->serialFd<0) return;

    serialFlush(this->serialFd);
}

HardwareSerial Serial;
