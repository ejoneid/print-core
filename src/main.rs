use axum::{Json, Router, http::StatusCode, routing::get, serve::Listener};
use serde_json::json;

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/health", get(health_check))
        .route("/files/cache", get(get_cache));

    let listener = tokio::net::TcpListener::bind("0.0.0.0:18000")
        .await
        .unwrap();

    axum::serve(listener, app).await;
}

async fn health_check() -> (StatusCode, Json<serde_json::Value>) {
    (StatusCode::OK, Json(json!({ "status": "ok" })))
}

async fn get_cache() -> &'static str {
    "Testing"
}
