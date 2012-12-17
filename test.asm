global main
extern print_int
extern print_str
extern print_char
extern read_int
extern read_char

segment .data


segment .text

main:
jmp hatta
jmp L0x2

hatta:
push rbp
mov rbp, rsp
push r8
push r9
push r10
push r11
push r12
push r13
push r14
mov r8, 1
mov r9, r8
mov r8, 2
mov r10, r8
mov r8, 3

mov rax, r9
add rax, r10
mov r9, rax

mov rax, r9
imul rax, r8
mov r8, rax
push r8
push r9
push r10
push r11
push r12
push r13
push r14
mov rdi, r8
call print_int
pop r14
pop r13
pop r12
pop r11
pop r10
pop r9
pop r8
L0x1:
pop r14
pop r13
pop r12
pop r11
pop r10
pop r9
pop r8
pop rbp
ret
L0x2:
