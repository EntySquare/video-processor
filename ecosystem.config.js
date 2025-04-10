module.exports = {
    apps: [{
      name: "video-processor",
      script: "uvicorn",
      args: "api:app --host 0.0.0.0 --port 8000",
      interpreter: "/root/miniconda3/envs/rt/bin/python",
      watch: ["./src"],
      ignore_watch: ["node_modules", "logs", "uploads", "outputs"],
      instances: 1,
      exec_mode: "fork",
      env: {
        NODE_ENV: "production"
      },
      log_date_format: "YYYY-MM-DD HH:mm:ss",
      error_file: "./logs/err.log",
      out_file: "./logs/out.log",
      merge_logs: true,
      max_memory_restart: "1G"
    }, {
      name: "video-processor-frontend",
      cwd: "./frontend",
      script: "npm",
      args: "start",
      instances: 1,
      exec_mode: "fork",
      env: {
        NODE_ENV: "production",
        PORT: 5000
      },
      log_date_format: "YYYY-MM-DD HH:mm:ss",
      error_file: "./logs/frontend-err.log",
      out_file: "./logs/frontend-out.log",
      merge_logs: true,
      max_memory_restart: "500M"
    }]
  }