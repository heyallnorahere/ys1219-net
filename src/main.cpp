#include "pch.h"
void index_handler(const drogon::HttpRequestPtr& request_pointer, std::function<void(const drogon::HttpResponsePtr&)>&& callback) {
    auto response = drogon::HttpResponse::newHttpResponse();
    response->addHeader("Content-Type", "text/html");
    response->setBody("<h1>Hello, world!</h1>");
    callback(response);
}
int32_t main(int32_t argc, const char** argv) {
    try {
        uint16_t port;
        std::string address;
        bool debug_enabled = true;
#ifdef NDEBUG
        debug_enabled = false;
#endif
        if (debug_enabled) {
            address = "127.0.0.1";
            port = 8080;
        } else {
            port = 443;
            address = "ys1219.net";
        }
        auto& app = drogon::app();
        app.registerHandler("/", std::function<void(const drogon::HttpRequestPtr&, std::function<void(const drogon::HttpResponsePtr&)>&&)>(index_handler), {drogon::Get});
        app.addListener(address, port);
        if (!app.supportSSL()) {
            throw std::runtime_error("drogon was not built correctly");
        }
        spdlog::info("hosting at: {0}:{1}", address, port);
        app.run();
        return 0;
    } catch (const std::runtime_error& exc) {
        spdlog::error(exc.what());
        return 1;
    }
}