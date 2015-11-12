# Path to your oh-my-zsh configuration.
#
ZSH=$HOME/.oh-my-zsh

# Set name of the theme to load.
# Look in ~/.oh-my-zsh/themes/
# Optionally, if you set this to "random", it'll load a random theme each
# time that oh-my-zsh is loaded.
ZSH_THEME="bira"


# Example aliases
#alias v="mvim"
#alias ats="source /cs/coursedata/cs520/environment"
#alias vimrc="emacs ~/.vimrc"
#alias emarc="vim ~/.emacs"
# alias ohmyzsh="mate ~/.oh-my-zsh"
alias brew="sudo brew"
alias sduo='sudo'
alias ema='emacs -daemon'
alias r='python ~/.ranger-1.7.1/ranger.py'
alias cls='clear && ls'
alias e="emacsclient -nw"
alias p="python"
#alias ="g++ test.cpp && ./a.out"
alias mgdb='mongod --dbpath /Users/archie/build/data'
alias leanote='sudo sh /User/archie/build/leanote/bin/run.sh'
alias javac="javac -J-Dfile.encoding=utf8"
alias grep="grep --color=auto"
alias -s html=mate   # 在命令行直接输入后缀为 html 的文件名，会在 sublime 中打开
alias -s rb=emacs     # 在命令行直接输入 ruby 文件，会在 sublime中打开
alias -s py=emacs    # 在命令行直接输入 python 文件，会用 emacs 中打开，以下类似
alias -s js=emacs
alias -s c=emacs
alias -s java=emacs
alias -s txt=emacs
alias -s gz='tar -xzvf'
alias -s tgz='tar -xzvf'
alias -s zip='unzip'
alias -s bz2='tar -xjvf'
alias GIT='git add --all && git commit -m "update " &&  git push '
#alias mv='mv -i'
alias ats='source /cs/coursedata/cs520/environment && emacs '
alias ls='ls -F --color=auto'
alias l='ls'
alias grep='grep --color=auto'
alias la='ls -a'
alias vim='emacsclient -nw'
#alias vim='emacs'
alias BREW='brew update && brew upgrade'
#alias rm='rmtrash'
alias sduo='sudo'
alias sudo='sudo' 
alias i-miss-u= 'cat I know this is hard, but you need to move on and fight.\n And...dont apologize, cause it is a sign of weakness.'
# Set to this to use case-sensitive completion
# CASE_SENSITIVE="true"

# Uncomment this to disable bi-weekly auto-update checks
# DISABLE_AUTO_UPDATE="true"

# Uncomment to change how often before auto-updates occur? (in days)
# export UPDATE_ZSH_DAYS=13

# Uncomment following line if you want to disable colors in ls
# DISABLE_LS_COLORS="true"

# Uncomment following line if you want to disable autosetting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment following line if you want to disable command autocorrection
# DISABLE_CORRECTION="true"

# Uncomment following line if you want red dots to be displayed while waiting for completion
# COMPLETION_WAITING_DOTS="true"

# Uncomment following line if you want to disable marking untracked files under
# VCS as dirty. This makes repository status check for large repositories much,
# much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment following line if you want to  shown in the command execution time stamp 
# in the history command output. The optional three formats: "mm/dd/yyyy"|"dd.mm.yyyy"|
# yyyy-mm-dd
# HIST_STAMPS="mm/dd/yyyy"

# Which plugins would you like to load? (plugins can be found in ~/.oh-my-zsh/plugins/*)
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
plugins=(git svn virtualenv)

source $ZSH/oh-my-zsh.sh

# User configuration
export LD_LIBRARY_PATH=$HOME/lib:$LD_LIBRARY_PATH
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/home/grad3/shwsun/.local/bin:/home/grad3/shwsun/local/bin"
export PATSHOME="/cs/coursedata/cs520/ats2-lang/"
#export MANPATH="/usr/local/man:$MANPATH"

# # Preferred editor for local and remote sessions
 if [[ -n $SSH_CONNECTION ]]; then
   export EDITOR='emacs'
 else
   export EDITOR='vim'
 fi

# Compilation flags
 export ARCHFLAGS="-arch x86_64"

# ssh
# export SSH_KEY_PATH="~/.ssh/dsa_id"


#export EDITOR="/usr/local/bin/mate -w"""

#################################################################3

#设置光标颜色
if [[ $TERM == xterm* ]] || [[ $TERM == *rxvt* ]]; then # {{{2 设置光标颜色
  cursorcolor () { echo -ne "\e]12;$*\007" }
elif [[ $TERM == screen* ]]; then
  if [[ -n "$TMUX" ]]; then
    cursorcolor () { echo -ne "\ePtmux;\e\e]12;$*\007\e\\" }
  else
    cursorcolor () { echo -ne "\eP\e]12;$*\007\e\\" }
  fi
fi

# the fuck help
#eval "$(thefuck --alias)"

#color{{{
autoload colors
colors
 
for color in RED GREEN YELLOW BLUE MAGENTA CYAN WHITE; do
eval _$color='%{$terminfo[bold]$fg[${(L)color}]%}'
eval $color='%{$fg[${(L)color}]%}'
(( count = $count + 1 ))
done
FINISH="%{$terminfo[sgr0]%}"
#}}}
 
#命令提示符

#RPROMPT=$(echo "$RED%D %T$FINISH")
#PROMPT=$(echo "$BLUE%M$GREEN%/$CYAN%n $_YELLOW>>>$FINISH ")"")"")


#PROMPT=$(echo "[$CYAN%n@$YELLOW%M:$GREEN%/$_YELLOW]>$FINISH ")
 
#PROMPT=$(echo "[$CYAN%n@$YELLOW%cchrisvoid:$GREEN%/$_YELLOW>>$FINISH ")
#标题栏、任务栏样式{{{
#case $TERM in (*xterm*|*rxvt*|(dt|k|E)term)
#precmd () { print -Pn "\e]0;%n@%M//%/\a" }
#preexec () { print -Pn "\e]0;%n@%M//%/\ $1\a" }
#;;
#esac
#}}}

 
#editor vim / emacs
export EDITOR=emacs

#shurufa
export XMODIFIERS="@im=fcitx"
export QT_MODULE=fcitx
export GTK_MODULE=fcitx
export LC_ALL=en_US.UTF-8    
export LANG=en_US.UTF-8  


#杂项 {{{
#允许在交互模式中使用注释  例如：
#cmd #这是注释
setopt INTERACTIVE_COMMENTS      
 
#启用自动 cd，输入目录名回车进入目录
#稍微有点混乱，不如 cd 补全实用
setopt AUTO_CD
 
#扩展路径
#/v/c/p/p => /var/cache/pacman/pkg
#setopt complete_in_word
 
#禁用 core dumps
limit coredumpsize 0
 
#Emacs风格 键绑定
bindkey -e
#bindkey -v
#设置 [DEL]键 为向后删除
#bindkey "\e[3~" delete-char
 
#以下字符视为单词的一部分
WORDCHARS='*?_-[]~=&;!#$%^(){}<>'
#}}}
 
#自动补全功能 {{{
setopt AUTO_LIST
setopt AUTO_MENU
#开启此选项，补全时会直接选中菜单项
setopt MENU_COMPLETE
 
autoload -U compinit
compinit
 
#自动补全缓存
#zstyle ':completion::complete:*' use-cache on
#zstyle ':completion::complete:*' cache-path .zcache
#zstyle ':completion:*:cd:*' ignore-parents parent pwd
 
#自动补全选项
zstyle ':completion:*' verbose yes
zstyle ':completion:*' menu select
zstyle ':completion:*:*:default' force-list always
zstyle ':completion:*' select-prompt '%SSelect:  lines: %L  matches: %M  [%p]'
 
zstyle ':completion:*:match:*' original only
zstyle ':completion::prefix-1:*' completer _complete
zstyle ':completion:predict:*' completer _complete
zstyle ':completion:incremental:*' completer _complete _correct
zstyle ':completion:*' completer _complete _prefix _correct _prefix _match _approximate
 
#路径补全
zstyle ':completion:*' expand 'yes'
zstyle ':completion:*' squeeze-shlashes 'yes'
zstyle ':completion::complete:*' '\\'
 
#彩色补全菜单
#eval $(dircolors -b)
export ZLSCOLORS="${LS_COLORS}"
zmodload zsh/complist
zstyle ':completion:*' list-colors ${(s.:.)LS_COLORS}
zstyle ':completion:*:*:kill:*:processes' list-colors '=(#b) #([0-9]#)*=0=01;31'
 
#修正大小写
zstyle ':completion:*' matcher-list '' 'm:{a-zA-Z}={A-Za-z}'
#错误校正
zstyle ':completion:*' completer _complete _match _approximate
zstyle ':completion:*:match:*' original only
zstyle ':completion:*:approximate:*' max-errors 1 numeric
 
#kill 命令补全
compdef pkill=kill
compdef pkill=killall
zstyle ':completion:*:*:kill:*' menu yes select
zstyle ':completion:*:*:*:*:processes' force-list always
zstyle ':completion:*:processes' command 'ps -au$USER'
 
#补全类型提示分组
zstyle ':completion:*:matches' group 'yes'
zstyle ':completion:*' group-name ''
zstyle ':completion:*:options' description 'yes'
zstyle ':completion:*:options' auto-description '%d'
zstyle ':completion:*:descriptions' format $'\e[01;33m -- %d --\e[0m'
zstyle ':completion:*:messages' format $'\e[01;35m -- %d --\e[0m'
zstyle ':completion:*:warnings' format $'\e[01;31m -- No Matches Found --\e[0m'
zstyle ':completion:*:corrections' format $'\e[01;32m -- %d (errors: %e) --\e[0m'
 
# cd ~ 补全顺序
zstyle ':completion:*:-tilde-:*' group-order 'named-directories' 'path-directories' 'users' 'expand'
#}}}
 
##行编辑高亮模式 {{{
# Ctrl+@ 设置标记，标记和光标点之间为 region
zle_highlight=(region:bg=magenta #选中区域
special:bold      #特殊字符
isearch:underline)#搜索时使用的关键字
#}}}
 
##空行(光标在行首)补全 "cd " {{{
user-complete(){
case $BUFFER in
"" )                       # 空行填入 "cd "
BUFFER="cd "
zle end-of-line
zle expand-or-complete
;;
"cd --" )                  # "cd --" 替换为 "cd +"
BUFFER="cd +"
zle end-of-line
zle expand-or-complete
;;
"cd +-" )                  # "cd +-" 替换为 "cd -"
BUFFER="cd -"
zle end-of-line
zle expand-or-complete
;;
* )
zle expand-or-complete
;;
esac
}
zle -N user-complete
bindkey "\t" user-complete
#}}}
 
##在命令前插入 sudo {{{
#定义功能
sudo-command-line() {
[[ -z $BUFFER ]] && zle up-history
[[ $BUFFER != sudo\ * ]] && BUFFER="sudo $BUFFER"
zle end-of-line                 #光标移动到行末
}
zle -N sudo-command-line
#定义快捷键为： [Esc] [Esc]
bindkey "\e\e" sudo-command-line
#}}}
 
#[Esc][h] man 当前命令时，显示简短说明
#alias run-help >&/dev/null && unalias run-help
#autoload run-help
unalias run-help
autoload run-help
HELPDIR=/usr/local/share/zsh/help

#历史命令 top10
alias top10='print -l  ${(o)history%% *} | uniq -c | sort -nr | head -n 10'
#}}}
 
#路径别名 {{{
#进入相应的路径时只要 cd ~xxx
hash -d 520="/home/grad3/shwsun/code/cs520-2015-fall-shwsun_/Assignment"
hash -d training="/Users/arch/training"
hash -d bu="/Users/arch/Desktop/BostonUniversity"
hash -d pub="/home/grad3/shwsun/Public"

hash -d Github="/Users/archie/sub-archie/Github"
hash -d lnpy="/Users/archie/sub-archie/Github/lnpy"
hash -d paper="/Users/archie/sub-archie/build/paper"
hash -d topcoder="/Users/archie/sub-archie/Github/topcoder"
hash -d cacup="/Users/archie/sub-archie/build/CareerCup"
hash -d b="/Users/archie/sub-archie/build"
hash -d vinzor="/Users/archie/sub-archie/build/vinzor"
hash -d cvblog="/Users/archie/sub-archie/build/githubblog/chris-void.github.io/_posts/2014"
hash -d cvdiary="/Users/archie/sub-archie/build/githubblog/chris-void.github.io/diary"
hash -d learnpy="/Users/archie/sub-archie/build/pyfiles/learnpython"
hash -d coursera="/Users/archie/sub-archie/build/coursera"
hash -d leetcode="/Users/archie/sub-archie/Github/leetcode"
hash -d codejam="/Users/archie/sub-archie/build/codejam"
hash -d algs4="/Users/archie/Desktop/ToDo/algs4"
hash -d openstack="/Users/archie/sub-archie/build/openstack"
hash -d study="/Users/archie/sub-archie/build/study/"
#}}}
 
##for Emacs {{{
#在 Emacs终端 中使用 Zsh 的一些设置 不推荐在 Emacs 中使用它
#if [[ "$TERM" == "dumb" ]]; then
#setopt No_zle
#PROMPT='%n@%M %/
#>>'
#alias ls='ls -F'
#fi
#}}}
 
#{{{自定义补全
#补全 ping
zstyle ':completion:*:ping:*' hosts 192.168.1.{1,50,51,100,101} www.google.com
 
#补全 ssh scp sftp 等
#zstyle -e ':completion::*:*:*:hosts' hosts 'reply=(${=${${(f)"$(cat {/etc/ssh_,~/.ssh/known_}hosts(|2)(N) /dev/null)"}%%[# ]*}//,/ })'
#}}}
 
#{{{ F1 计算器
arith-eval-echo() {
LBUFFER="${LBUFFER}echo \$(( "
RBUFFER=" ))$RBUFFER"
}
zle -N arith-eval-echo
bindkey "^[[11~" arith-eval-echo
#}}}
 
####{{{
function timeconv { date -d @$1 +"%Y-%m-%d %T" }
 
# }}}
 
zmodload zsh/mathfunc
autoload -U zsh-mime-setup
zsh-mime-setup
setopt EXTENDED_GLOB
#autoload -U promptinit
#promptinit
#prompt redhat
 
setopt correctall
autoload compinstall
 
#漂亮又实用的命令高亮界面
setopt extended_glob
 TOKENS_FOLLOWED_BY_COMMANDS=('|' '||' ';' '&' '&&' 'sudo' 'do' 'time' 'strace')
 
 recolor-cmd() {
     region_highlight=()
     colorize=true
     start_pos=0
     for arg in ${(z)BUFFER}; do
         ((start_pos+=${#BUFFER[$start_pos+1,-1]}-${#${BUFFER[$start_pos+1,-1]## #}}))
         ((end_pos=$start_pos+${#arg}))
         if $colorize; then
             colorize=false
             res=$(LC_ALL=C builtin type $arg 2>/dev/null)
             case $res in
                 *'reserved word'*)   style="fg=magenta,bold";;
                 *'alias for'*)       style="fg=cyan,bold";;
                 *'shell builtin'*)   style="fg=yellow,bold";;
                 *'shell function'*)  style='fg=green,bold';;
                 *"$arg is"*)
                     [[ $arg = 'sudo' ]] && style="fg=red,bold" || style="fg=blue,bold";;
                 *)                   style='none,bold';;
             esac
             region_highlight+=("$start_pos $end_pos $style")
         fi
         [[ ${${TOKENS_FOLLOWED_BY_COMMANDS[(r)${arg//|/\|}]}:+yes} = 'yes' ]] && colorize=true
         start_pos=$end_pos
     done
 }
check-cmd-self-insert() { zle .self-insert && recolor-cmd }
 check-cmd-backward-delete-char() { zle .backward-delete-char && recolor-cmd }
 
 zle -N self-insert check-cmd-self-insert
 zle -N backward-delete-char check-cmd-backward-delete-char


[[ -s ~/.autojump/etc/profile.d/autojump.sh ]] && . ~/.autojump/etc/profile.d/autojump.sh

#export PATH~/.cabal/bin:$PATH
export PREFIX_PATH=~/.pypkg:$PREFIX_PATH
#PATH=$PATH:$HOME/.rvm/bin # Add RVM to PATH for scripting
#export PATH=/usr/local/sbin:$PATH
#eval $(thefuck --alias)
