global main
extern print_int
extern print_str
extern print_char
extern read_int
extern read_char

segment .data

str1 db `Which term in the Fibonacci sequence shall I compute?`, 0
str2 db `Fib number `, 0
str3 db ` = `, 0

segment .text

main:
jmp hatta
jmp L0x2

fibonacci0x1:
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
mov r9, [rbp+16]
mov r8, 0
mov r11, r8
mov r8, 1
mov r12, r8
mov r8, 0
mov r10, r8
L0x5:
cmp r10, r9
jge L0x7
L0x6:
mov r8, r11
mov r11, r12
mov rax, r8
add rax, r12
mov r8, rax
mov r12, r8
mov rax, r10
add rax, 1
mov r10, rax
jmp L0x5
L0x7:
mov rax, r11
jmp L0x1
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
jmp L0xb

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
call fibonacci0x1
add rsp, 8
mov r8, rax
mov r10, r8
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
