resource "local_file" "502" {
  content  = var.html_content_502
  filename = "${path.module}/sources/502.html"
}

resource "local_file" "503" {
  content  = var.html_content_503
  filename = "${path.module}/sources/503.html"
}