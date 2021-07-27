#include <iostream>
#include <acme-lw.h>
int main(int argc, const char** argv)
{
    acme_lw::AcmeClient::init();
    acme_lw::AcmeClient::teardown();
    return 0;
}