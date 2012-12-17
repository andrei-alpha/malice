global main
extern print_int
extern print_str
extern print_char
extern read_int
extern read_char

segment .data

arr1 dq 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
str1 db ` is prime\n`, 0
str2 db ` is NOT prime\n`, 0
str3 db `There are `, 0
str4 db ` primes in the first `, 0
str5 db ` natural numbers`, 0

segment .text

main:
mov r8, 10
mov r13, r8
jmp hatta
jmp L0x3

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
jmp L0x5

initialise0x1:
push rbp
mov rbp, rsp
push r8
push r9
push r10
push r11
push r12
push r13
push r14
mov r8, 0
mov r12, r8
L0x6:
cmp r12, r13
je L0x8
L0x7:
mov r10, 0
cmp r12, r10
je L0xe
mov r9, 1
cmp r12, r9
je L0xe
L0xe:
mov r11, 0
mov rax, arr1
mov [rax+8*r12], r11
jmp L0xa
L0xc:
mov r8, 1
mov rax, arr1
mov [rax+8*r12], r8
jmp L0xa
L0xa:
mov rax, r12
add rax, 1
mov r12, rax
jmp L0x6
L0x8:
L0x4:
pop r14
pop r13
pop r12
pop r11
pop r10
pop r9
pop r8
pop rbp
ret
L0x5:
jmp L0x13

findPrimes0x2:
push rbp
mov rbp, rsp
push r8
push r9
push r10
push r11
push r12
push r13
push r14
jmp L0x15

output0x3:
push rbp
mov rbp, rsp
push r8
push r9
push r10
push r11
push r12
push r13
push r14
mov r10, 0
mov r8, r10
mov r9, 0
mov r12, r9
L0x17:
cmp r12, r13
je L0x19
L0x18:
mov r11, 1
cmp arr, r11
jne L0x1d
L0x1f:
push r8
push r9
push r10
push r11
push r12
push r13
push r14
mov rdi, r12
call print_int
pop r14
pop r13
pop r12
pop r11
pop r10
pop r9
pop r8
mov r9, str1
push r8
push r9
push r10
push r11
push r12
push r13
push r14
mov rdi, r9
call print_str
pop r14
pop r13
pop r12
pop r11
pop r10
pop r9
pop r8
mov rax, r8
add rax, 1
mov r8, rax
jmp L0x1b
L0x1d:
push r8
push r9
push r10
push r11
push r12
push r13
push r14
mov rdi, r12
call print_int
pop r14
pop r13
pop r12
pop r11
pop r10
pop r9
pop r8
mov r9, str2
push r8
push r9
push r10
push r11
push r12
push r13
push r14
mov rdi, r9
call print_str
pop r14
pop r13
pop r12
pop r11
pop r10
pop r9
pop r8
jmp L0x1b
L0x1b:
mov rax, r12
add rax, 1
mov r12, rax
jmp L0x17
L0x19:
mov rax, r8
jmp L0x14
L0x14:
pop r14
pop r13
pop r12
pop r11
pop r10
pop r9
pop r8
pop rbp
ret
L0x15:
mov r15, 2
mov r12, r15
L0x23:
mov rax, r12
imul rax, r12
mov r9, rax
cmp r9, r13
jge L0x25
L0x24:
mov r10, 1
cmp arr, r10
jne L0x27
L0x2b:
mov r16, r12
L0x2e:
mov rax, r12
imul rax, r16
mov r11, rax
cmp r11, r13
jge L0x30
L0x2f:
mov rax, r12
imul rax, r16
mov r14, rax
mov r8, 0
mov rax, arr1
mov [rax+8*r14], r8
mov rax, r16
add rax, 1
mov r16, rax
jmp L0x2e
L0x30:
jmp L0x27
L0x27:
mov rax, r12
add rax, 1
mov r12, rax
jmp L0x23
L0x25:
call output0x3
add rsp, 0
mov r9, rax
mov r8, r9
mov r9, str3
push r8
push r9
push r10
push r11
push r12
push r13
push r14
mov rdi, r9
call print_str
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
mov rdi, r8
call print_int
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
mov rdi, r8
call print_str
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
mov rdi, r13
call print_int
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
mov rdi, r8
call print_str
pop r14
pop r13
pop r12
pop r11
pop r10
pop r9
pop r8
L0x12:
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
call initialise0x1
add rsp, 0
call findPrimes0x2
add rsp, 0
L0x2:
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
