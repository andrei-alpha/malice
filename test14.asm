global main
extern print_int
extern print_str
extern print_char
extern read_int
extern read_char

segment .data

str1 db `arr[`, 0
str2 db `] = `, 0
str3 db `\n`, 0
arr1 dq 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0

segment .text

main:
mov r9, 100
mov r11, r9
jmp hatta
jmp L0x3

output:
push rbp
mov rbp, rsp
push r8
push r9
push r10
push r11
push r12
push r13
push r14
push r15
mov r9, 0

L0x5:
cmp r9, r11
je L0x7
L0x6:
mov r10, str1
push r8
push r9
push r10
push r11
push r12
push r13
push r14
push r15
mov rdi, r10
call print_str
pop r15
pop r14
pop r13
pop r12
pop r11
pop r10
pop r9
pop r8
push r8
push r9
push r10
push r11
push r12
push r13
push r14
push r15
mov rdi, r9
call print_int
pop r15
pop r14
pop r13
pop r12
pop r11
pop r10
pop r9
pop r8
mov r10, str2
push r8
push r9
push r10
push r11
push r12
push r13
push r14
push r15
mov rdi, r10
call print_str
pop r15
pop r14
pop r13
pop r12
pop r11
pop r10
pop r9
pop r8
push r8
push r9
push r10
push r11
push r12
push r13
push r14
push r15
mov rdi, r8
mov rdi, [rdi+8*r9]
call print_int
pop r15
pop r14
pop r13
pop r12
pop r11
pop r10
pop r9
pop r8
mov r10, str3
push r8
push r9
push r10
push r11
push r12
push r13
push r14
push r15
mov rdi, r10
call print_str
pop r15
pop r14
pop r13
pop r12
pop r11
pop r10
pop r9
pop r8
mov rax, r9
add rax, 1
mov r9, rax
jmp L0x5
L0x7:
L0x2:
pop r15
pop r14
pop r13
pop r12
pop r11
pop r10
pop r9
pop r8
pop rbp
ret
L0x3:
jmp L0xb

initialise2:
push rbp
mov rbp, rsp
push r8
push r9
push r10
push r11
push r12
push r13
push r14
push r15
mov r8, [rbp+24]
mov r9, r8
L0xd:
cmp r9, r11
je L0xf
L0xe:
mov r8, 2
mov rax, r10
mov [rax+8*r9], r8
mov rax, r9
add rax, 1
mov r9, rax
jmp L0xd
L0xf:
push $R14
call output
add rsp, 8
L0xa:
pop r15
pop r14
pop r13
pop r12
pop r11
pop r10
pop r9
pop r8
pop rbp
ret
L0xb:
jmp L0x13

initialise:
push rbp
mov rbp, rsp
push r8
push r9
push r10
push r11
push r12
push r13
push r14
push r15
mov r8, 0
mov r9, r8
L0x15:
mov r8, 2
mov rax, r11
mov rdx, 0
idiv r8
mov r8, rax
cmp r9, r8
je L0x17
L0x16:
mov r8, 1
mov rax, r10
mov [rax+8*r9], r8
mov rax, r9
add rax, 1
mov r9, rax
jmp L0x15
L0x17:
push r9
push $R16
call initialise2
add rsp, 16
L0x12:
pop r15
pop r14
pop r13
pop r12
pop r11
pop r10
pop r9
pop r8
pop rbp
ret
L0x13:
jmp L0x1b

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
push r15
mov rax, arr1
push rax
call initialise
add rsp, 8
L0x1a:
pop r15
pop r14
pop r13
pop r12
pop r11
pop r10
pop r9
pop r8
pop rbp
ret
L0x1b:
