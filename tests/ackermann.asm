global main
extern print_int
extern print_str
extern print_char
extern read_int
extern read_char

segment .data

str1 db `Enter the first number`, 0
str2 db `Enter the second number`, 0
str3 db `ackermann(`, 0
str4 db `,`, 0
str5 db `) = `, 0

segment .text

main:
jmp hatta
jmp L0x2

ackermann0x1:
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
mov r10, [rbp+16]
mov r9, [rbp+24]
mov r8, 0
cmp r10, r8
jne L0x6
L0x7:
mov r8, 1
mov rax, r9
add rax, r8
mov r8, rax
mov rax, r8
jmp L0x1
jmp L0x3
L0x6:
mov r8, 0
cmp r10, r8
jle L0x9
mov r8, 0
cmp r9, r8
jne L0x9
L0xa:
mov r8, 1
mov rax, r10
sub rax, r8
mov r9, rax
mov r8, 1
push r8
push r9
call ackermann0x1
add rsp, 16
mov r8, rax
mov rax, r8
jmp L0x1
jmp L0x3
L0x9:
mov r8, 0
cmp r10, r8
jle L0x3
mov r8, 0
cmp r9, r8
jle L0x3
L0xe:
mov r8, 1
mov rax, r10
sub rax, r8
mov r8, rax
mov r8, 1
mov rax, r9
sub rax, r8
mov r8, rax
push r8
push r10
call ackermann0x1
add rsp, 16
mov r9, rax
push r9
push r8
call ackermann0x1
add rsp, 16
mov r8, rax
mov rax, r8
jmp L0x1
jmp L0x3
L0x3:
L0x1:
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
L0x2:
jmp L0x12

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
mov r8, str1
push r8
push r9
push r10
push r11
push r12
push r13
push r14
push r15
mov rdi, r8
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
push r11
push r12
push r13
push r14
push r15
call read_int
mov r10, rax
pop r15
pop r14
pop r13
pop r12
pop r11
pop r9
pop r8
mov r8, str2
push r8
push r9
push r10
push r11
push r12
push r13
push r14
push r15
mov rdi, r8
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
push r10
push r11
push r12
push r13
push r14
push r15
call read_int
mov r9, rax
pop r15
pop r14
pop r13
pop r12
pop r11
pop r10
pop r8
push r9
push r10
call ackermann0x1
add rsp, 16
mov r8, rax
mov r11, r8
mov r8, str3
push r8
push r9
push r10
push r11
push r12
push r13
push r14
push r15
mov rdi, r8
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
mov rdi, r10
call print_int
pop r15
pop r14
pop r13
pop r12
pop r11
pop r10
pop r9
pop r8
mov r8, str4
push r8
push r9
push r10
push r11
push r12
push r13
push r14
push r15
mov rdi, r8
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
mov r8, str5
push r8
push r9
push r10
push r11
push r12
push r13
push r14
push r15
mov rdi, r8
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
mov rdi, r11
call print_int
pop r15
pop r14
pop r13
pop r12
pop r11
pop r10
pop r9
pop r8
L0x11:
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
L0x12:
