#include <drogon/drogon.h>
void index_handler(const drogon::HttpRequestPtr& request_pointer, std::function<void(const drogon::HttpResponsePtr&)>&& callback) {
    auto response = drogon::HttpResponse::newHttpResponse();
    response->addHeader("Content-Type", "text/html");
    response->setBody("<h1>Hello, world!</h1>");
    callback(response);
}
int main(int argc, const char** argv) {
    auto& app = drogon::app();
    app.registerHandler("/", std::function<void(const drogon::HttpRequestPtr&, std::function<void(const drogon::HttpResponsePtr&)>&&)>(index_handler), {drogon::Get});
    app.addListener("127.0.0.1", 8080).run();
    return 0;
}