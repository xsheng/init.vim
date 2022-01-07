" https://github.com/zenbro/dotfiles/blob/master/.nvimrc
set nocompatible              " be improved, required
filetype off                  " required
chdir ~			      " change the dir to ~

"{{{ set <leader> as <space>, ; as :
let mapleader=" "
"}}}

"{{{ copy from system clispboard
" turn on the shift-insert behavior for windows
map! <s-insert>  <c-r>+
" "+p will paste from the system clipboard
" "+y will copy to it
" }}}

"{{{ general settings
set mouse=a " to enable mouse for visual selection
set scrolloff=999 " keep cursor at the middle of screen
set cursorline " show the cursorline 
set visualbell " disable sound bell
set nowrap " don't wrap long lines
nnoremap <leader> w :w<cr>
nnoremap <leader> q :q!<cr>
set undolevels=5000 "set maximum undo levels
set ruler "turn on ruler on the status line
set colorcolumn=77
highlight! colorcolumn ctermbg=233 guibg=#131313
" various columns
highlight! signcolumn ctermbg=233 guibg=#0d0d0d
highlight! foldcolumn ctermbg=233 guibg=#0d0d0d
" disable search highlighting
nnoremap <silent> <esc><esc> :nohlsearch<cr><esc>
" }}}

" cursor configuration {{{
" ====================================================================
" use a blinking upright bar cursor in insert mode, a solid block in normal
" and a blinking underline in replace mode
let $nvim_tui_enable_cursor_shape=1
let &t_si = "\<esc>[5 q"
let &t_sr = "\<esc>[3 q"
let &t_ei = "\<esc>[2 q"
" }}}


" {{{{ vundle
" set the runtime path to include vundle and initialize
set rtp+=~/.vim/bundle/vundle.vim
call vundle#begin()
" alternatively, pass a path where vundle should install plugins
"call vundle#begin('~/some/path/here')

" let vundle manage vundle, required
plugin 'vundlevim/vundle.vim'

" the following are examples of different formats supported.
" keep plugin commands between vundle#begin/end.
" plugin on github repo
plugin 'tpope/vim-fugitive'
plugin 'aserebryakov/vim-todo-lists'
" plugin from http://vim-scripts.org/vim/scripts.html
" plugin 'l9'
" git plugin not hosted on github
plugin 'git://git.wincent.com/command-t.git'
" git repos on your local machine (i.e. when working on your own plugin)
" plugin 'file:///home/gmarik/path/to/plugin'
" the sparkup vim script is in a subdirectory of this repo called vim.
" pass the path to set the runtimepath properly.

plugin 'rstacruz/sparkup', {'rtp': 'vim/'}
" install l9 and avoid a naming conflict if you've already installed a
" different version somewhere else.
" plugin 'ascenator/l9', {'name': 'newl9'}

plugin 'inkarkat/vim-extractmatches'

" "grammar check
" plugin 'rhysd/vim-grammarous' "this plugin requires java 8

" grammar check with languagetool.org
" it requires the languagetool to be installed first
plugin 'dpelle/vim-languagetool'

"lightline, fancy statusline
plugin 'itchyny/lightline.vim'

"nerdtree
plugin 'preservim/nerdtree'

"{{{fzf
plugin 'junegunn/fzf', { 'do': { -> fzf#install() } }
plugin 'junegunn/fzf.vim'
plugin 'airblade/vim-rooter'
"}}}

"ag
"plugin 'numkil/ag.nvim'

" markdown
" {{{
" plugin 'suan/vim-instant-markdown', {'for': 'markdown'}
plugin 'godlygeek/tabular'
plugin 'plasticboy/vim-markdown'
"plugin 'gabrielelana/vim-markdown'
plugin 'dhruvasagar/vim-table-mode', { 'on': 'tablemodetoggle', 'for': ['text', 'markdown', 'vim-plug'] }
plugin 'mzlogin/vim-markdown-toc', { 'for': ['gitignore', 'markdown', 'vim-plug'] }
plugin 'iamcco/markdown-preview.nvim' 
plugin 'dkarter/bullets.vim'
"markdown preview
plugin 'euclio/vim-markdown-composer'
" }}}
" {{{ xtabline
" plugin 'mg979/vim-xtabline'
" all of your plugins must be added before the following line
call vundle#end()            " required
"}}}}

" brief help
" :pluginlist       - lists configured plugins
" :plugininstall    - installs plugins; append `!` to update or just :pluginupdate
" :pluginsearch foo - searches for foo; append `!` to refresh local cache
" :pluginclean      - confirms removal of unused plugins; append `!` to auto-approve removal
"
" see :h vundle for more details or wiki for faq
" put your non-plugin stuff after this line
" to ignore plugin indent changes, instead use:
"filetype plugin on
"

"{{{nerdtree settings
nnoremap <leader>n :nerdtreefocus<cr>
nnoremap <c-n> :nerdtree<cr>
nnoremap <c-t> :nerdtreetoggle<cr>
nnoremap <c-f> :nerdtreefind<cr>
"}}}


filetype plugin indent on    " required
set rnu "relative number
set nu "line number
set noswapfile
set nobackup
syntax on
set spell spelllang=en_us
"set guifont=courier_new:h12:b
set guifont=consolas:h12
set hlsearch
colorscheme evening "morning
set guioptions-=t "disable toolbar

" {{{ markdown settings
let g:markdown_composer_autostart = 0 " this is to prevent a new browser tab for markdown preview
"{{vim-markdown-toc
"let g:vmt_auto_update_on_save = 0
"let g:vmt_dont_insert_fence = 1
let g:vmt_cycle_list_item_markers = 1
let g:vmt_fence_text = 'toc'
let g:vmt_fence_closing_text = '/toc'
noremap <leader>ms :markdownpreviewstop<cr>
"}}
let g:vim_markdown_math = 1
"let g:vim_markdown_fenced_languages = ['csharp=cs', 'python=py']
"noremap <leader>e :markdowneditcodeblock<cr>
"}}}


" open the vimrc file anytime
"
noremap <leader>rc :e ~\appdata\local\nvim\init.vim<cr>
noremap <leader>rn :exe 'edit '.stdpath('config').'/init.vim'<cr>
noremap <leader>rv :e ~\_vimrc<cr>
noremap <leader>so :source ~\_vimrc<cr>
" % means current buffer

" {{{ folding
noremap <silent> <leader>o za
"}}}

"{{{ compile function
noremap <leader>r :call compilerungcc()<cr>
func! compilerungcc()
	"execute write function first
	exec "w"
	if &filetype == 'python'
		set splitbelow
		:sp
		:term python3 %
	elseif &filetype == 'html'
		silent! exec "!".g:mkdp_browser." % &"
	elseif &filetype == 'markdown'
		silent! exec "markdownpreview"
	elseif &filetype == 'tex'
		silent! exec "vimtexstop"
		silent! exec "vimtexcompile"
	endif
endfunc
"}}}

" vim rooter
let g:rooter_target = '*' " this is all files
