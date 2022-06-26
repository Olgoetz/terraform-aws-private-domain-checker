
resource "null_resource" "python" {
  provisioner "local-exec" {
    command = "pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org install requests --target './sources/python'"
  }
}

data "archive_file" "python" {
  depends_on  = [null_resource.python]
  type        = "zip"
  source_dir  = "${path.module}/sources"
  output_path = "${path.module}/python_packages.zip"
}
resource "aws_lambda_layer_version" "python" {
  filename   = data.archive_file.python.output_path
  layer_name = "TFE-Lambda-Layer-Python"

  compatible_runtimes = ["python3.9"]
}


