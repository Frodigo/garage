return {
  {
    "nvim-treesitter/nvim-treesitter",
    build = ":TSUpdate",
    config = function()
      require 'nvim-treesitter.configs'.setup {
        -- A list of parser names, or "all" (the listed parsers MUST always be installed)
        ensure_installed = { "bash", "c", "c_sharp", "csv", "css", "dockerfile", "go", "html", "http", "javascript", "json", "lua", "sql", "terraform", "typescript", "vim", "vimdoc", "vue", "xml", "yaml", "query", "markdown", "markdown_inline", "python" },
        auto_install = true,
        highlight = {
          enable = true,
          disable = function(lang, buf)
            local max_filesize = 100 * 1024 -- 100 KB
            local ok, stats = pcall(vim.loop.fs_stat, vim.api.nvim_buf_get_name(buf))
            if ok and stats and stats.size > max_filesize then
              return true
            end
          end,

          additional_vim_regex_highlighting = true,
        },
      }
    end,
  }
}
