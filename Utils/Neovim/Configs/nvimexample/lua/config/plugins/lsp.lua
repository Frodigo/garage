return {
	{
		"neovim/nvim-lspconfig",
		dependencies = {
			"folke/lazydev.nvim",
			ft = "lua", -- only load on lua files
			opts = {
				library = {
					-- See the configuration section for more details
					-- Load luvit types when the `vim.uv` word is found
					{ path = "${3rd}/luv/library", words = { "vim%.uv" } },
				},
			},
		},

		config = function()
			require('lspconfig').lua_ls.setup {
				diagnostics = {
					globals = { 'vim' }
				},

				require('lspconfig').pyright.setup {},

				vim.api.nvim_create_autocmd('LspAttach', {
					group = vim.api.nvim_create_augroup('my.lsp', {}),
					callback = function(args)
						local client = assert(vim.lsp.get_client_by_id(args.data.client_id))
						if client:supports_method('textDocument/implementation') then
							-- Create a keymap for vim.lsp.buf.implementation ...
						end

						-- Enable auto-completion. Note: Use CTRL-Y to select an item. |complete_CTRL-Y|
						-- if client:supports_method('textDocument/completion') then
						-- Optional: trigger autocompletion on EVERY keypress. May be slow!
						-- local chars = {}; for i = 32, 126 do table.insert(chars, string.char(i)) end
						-- client.server_capabilities.completionProvider.triggerCharacters = chars

						--	vim.lsp.completion.enable(true, client.id, args.buf, { autotrigger = true })
						-- end

						-- Auto-format ("lint") on save.
						-- Usually not needed if server supports "textDocument/willSaveWaitUntil".
						if not client:supports_method('textDocument/willSaveWaitUntil')
								and client:supports_method('textDocument/formatting') then
							vim.api.nvim_create_autocmd('BufWritePre', {
								group = vim.api.nvim_create_augroup('my.lsp', { clear = false }),
								buffer = args.buf,
								callback = function()
									vim.lsp.buf.format({ bufnr = args.buf, id = client.id, timeout_ms = 1000 })
								end,
							})
						end
					end,
				}),
			}
		end,
	}
}
