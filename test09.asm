global main
extern print_int
extern print_str
extern print_char
extern read_int
extern read_char

segment .data

str1 db ` is biggest\n`, 0
str2 db ` is biggest\n`, 0
str3 db ` is biggest\n`, 0
str4 db ` is biggest\n`, 0
str5 db ` are equal \n`, 0
str6 db `Enter a number`, 0
str7 db `Enter a number`, 0
str8 db `Enter a number`, 0

segment .text

main:
jmp hatta
jmp L0x2

compare:
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
cmp r10, r8
jle L0x5
L0x7:
cmp r10, r9
jle L0xb
L0xd:
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
jmp L0x9
L0xb:
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
jmp L0x9
L0x9:
jmp L0x3
L0x5:
cmp r8, r9
jle L0x12
L0x13:
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
jmp L0xf
L0x12:
cmp r9, r8
jle L0x11
L0x16:
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
jmp L0xf
L0x11:
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
jmp L0xf
L0xf:
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
jmp L0x19

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
mov r11, str6
push r8
push r9
push r10
push r11
push r12
push r13
push r14
push r15
mov rdi, r11
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
mov r10, str7
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
push r9
push r10
push r11
push r12
push r13
push r14
push r15
call read_int
mov r8, rax
pop r15
pop r14
pop r13
pop r12
pop r11
pop r10
pop r9
mov r8, str8
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
call compare
add rsp, 0
L0x18:
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
L0x19:
