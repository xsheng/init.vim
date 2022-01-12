" https://github.com/zenbro/dotfiles/blob/master/.nvimrc
set nocompatible              " be iMproved, required
" filetype off                  " required
chdir ~ " change the dir to ~

"{{{ Set <LEADER> as <SPACE>, ; as :
let mapleader=" "
"}}}

"{{{ Copy from system clipboard
" turn on the shift-insert behavior for windows
map! <S-Insert>  <C-R>+
" "+p will paste from the system clipboard
" "+y will copy to it
" }}}

"{{{ General settings
" ====================================================================
set mouse=a " to enable mouse for visual selection
set scrolloff=999 " keep cursor at the middle of screen
set cursorline " show the cursorline 
set visualbell " disable sound bell
set nowrap " don't wrap long lines
nnoremap <LEADER> w :w<Enter>
nnoremap <LEADER> q :q!<Enter>
set undolevels=5000 "set maximum undo levels
set ruler "turn on ruler on the status line
set colorcolumn=77
highlight! ColorColumn ctermbg=233 guibg=#131313
" Various columns
highlight! SignColumn ctermbg=233 guibg=#0D0D0D
highlight! FoldColumn ctermbg=233 guibg=#0D0D0D
" Disable search highlighting
nnoremap <silent> <Esc><Esc> :nohlsearch<CR><Esc>
" }}}

" Cursor configuration {{{
" ====================================================================
" Use a blinking upright bar cursor in Insert mode, a solid block in normal
" and a blinking underline in replace mode
let $NVIM_TUI_ENABLE_CURSOR_SHAPE=1
let &t_SI = "\<Esc>[5 q"
let &t_SR = "\<Esc>[3 q"
let &t_EI = "\<Esc>[2 q"
" }}}


" {{{{ Vundle
" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
" alternatively, pass a path where Vundle should install plugins
"call vundle#begin('~/some/path/here')

" let Vundle manage Vundle, required
Plugin 'VundleVim/Vundle.vim'

" The following are examples of different formats supported.
" Keep Plugin commands between vundle#begin/end.
" plugin on GitHub repo
Plugin 'tpope/vim-fugitive'
Plugin 'aserebryakov/vim-todo-lists'
" plugin from http://vim-scripts.org/vim/scripts.html
" Plugin 'L9'
" Git plugin not hosted on GitHub
Plugin 'git://git.wincent.com/command-t.git'
" command-t requires ruby...
" git repos on your local machine (i.e. when working on your own plugin)
" Plugin 'file:///home/gmarik/path/to/plugin'
" The sparkup vim script is in a subdirectory of this repo called vim.
" Pass the path to set the runtimepath properly.

Plugin 'rstacruz/sparkup', {'rtp': 'vim/'}
" Install L9 and avoid a Naming conflict if you've already installed a
" different version somewhere else.
" Plugin 'ascenator/L9', {'name': 'newL9'}

Plugin 'inkarkat/vim-ExtractMatches'

" "Grammar check
" Plugin 'rhysd/vim-grammarous' "this plugin requires Java 8

" Grammar check with Languagetool.org
" it requires the Languagetool to be installed first
Plugin 'dpelle/vim-LanguageTool'

"lightline, fancy statusline
Plugin 'itchyny/lightline.vim'

"NERDTree
Plugin 'preservim/nerdtree'
"{{{NERDTree settings
    nnoremap <leader>n :NERDTreeFocus<CR>
    nnoremap <C-n> :NERDTree<CR>
    nnoremap <C-t> :NERDTreeToggle<CR>
    nnoremap <C-f> :NERDTreeFind<CR>
"}}}

"{{{FZF
Plugin 'junegunn/fzf', { 'do': { -> fzf#install() } }
Plugin 'junegunn/fzf.vim'
Plugin 'airblade/vim-rooter'
"}}}

"ag
"Plugin 'numkil/ag.nvim'

" Markdown
" {{{
" Plugin 'suan/vim-instant-markdown', {'for': 'markdown'}
Plugin 'godlygeek/tabular'
Plugin 'plasticboy/vim-markdown'
"Plugin 'gabrielelana/vim-markdown'
Plugin 'dhruvasagar/vim-table-mode', { 'on': 'TableModeToggle', 'for': ['text', 'markdown', 'vim-plug'] }
Plugin 'mzlogin/vim-markdown-toc', { 'for': ['gitignore', 'markdown', 'vim-plug'] }
Plugin 'iamcco/markdown-preview.nvim' 
Plugin 'dkarter/bullets.vim'
"Markdown preview
Plugin 'euclio/vim-markdown-composer'
" }}}
" {{{ xtabline
" Plugin 'mg979/vim-xtabline'
"
" Indent visualization
Plugin 'nathanaelkane/vim-indent-guides'
" {{{ indent settings
    let g:indent_guides_enable_on_vim_startup = 1
    let g:indent_guides_auto_colors = 1
    set ts=4 sw=4 et
    let g:indent_guides_start_level = 1
    let g:indent_guides_guide_size = 1
    "autocmd VimEnter,Colorscheme * :hi IndentGuidesOdd  guibg=grey   ctermbg=3
    "autocmd VimEnter,Colorscheme * :hi IndentGuidesEven guibg=grey ctermbg=4
" }}}

" All of your Plugins must be added before the following line
call vundle#end()            " required
"}}}}

" Brief help
" :PluginList       - lists configured plugins
" :PluginInstall    - installs plugins; append `!` to update or just :PluginUpdate
" :PluginSearch foo - searches for foo; append `!` to refresh local cache
" :PluginClean      - confirms removal of unused plugins; append `!` to auto-approve removal
"
" see :h Vundle for more details or wiki for FAQ
" Put your non-Plugin stuff after this line
" To ignore plugin indent changes, instead use:
"filetype plugin on
"



filetype plugin indent on    " required
set rnu "relative number
set nu "line number
set noswapfile
set nobackup
syntax on
set spell spelllang=en_us
"set guifont=courier_new:h12:b
set guifont=Consolas:h12
set hlsearch
colorscheme evening "morning
set guioptions-=T "disable toolbar

" {{{ Markdown settings
let g:markdown_composer_autostart = 0 " this is to prevent a new browser tab for markdown preview
"{{vim-markdown-toc
"let g:vmt_auto_update_on_save = 0
"let g:vmt_dont_insert_fence = 1
let g:vmt_cycle_list_item_markers = 1
let g:vmt_fence_text = 'TOC'
let g:vmt_fence_closing_text = '/TOC'
noremap <LEADER>ms :MarkdownPreviewStop<CR>
"}}
let g:vim_markdown_math = 1
"let g:vim_markdown_fenced_languages = ['csharp=cs', 'python=py']
"noremap <LEADER>e :MarkdownEditCodeBlock<CR>
"}}}


" Open the vimrc file anytime
"
noremap <LEADER>rc :e ~\AppData\Local\nvim\init.vim<CR>
noremap <LEADER>rn :exe 'edit '.stdpath('config').'/init.vim'<CR>
noremap <LEADER>rv :e ~\_vimrc<CR>
noremap <LEADER>so :source ~\_vimrc<CR>
" % means current buffer

" {{{ Folding
noremap <silent> <LEADER>o za
"}}}

"{{{ Compile function
noremap <LEADER>r :call CompileRunGcc()<CR>
func! CompileRunGcc()
	"execute write function first
	exec "w"
	if &filetype == 'python'
		set splitbelow
		:sp
		:term python3 %
	elseif &filetype == 'html'
		silent! exec "!".g:mkdp_browser." % &"
	elseif &filetype == 'markdown'
		silent! exec "MarkdownPreview"
	elseif &filetype == 'tex'
		silent! exec "VimtexStop"
		silent! exec "VimtexCompile"
	endif
endfunc
"}}}

" vim rooter
let g:rooter_target = '*' " this is All files
