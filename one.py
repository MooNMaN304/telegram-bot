# import dis

# def one(x, y):
#     return x + y

# print(dis.dis(one))

# '''
#   3           0 RESUME                   0

#   4           2 LOAD_FAST                0 (x)
#               4 LOAD_FAST                1 (y)
#               6 BINARY_OP                0 (+)
#              10 RETURN_VALUE
# '''

# list_with_functions = {'BINARY_OP': one}
# "https://github.com/python/cpython"


# """
# section .text
#     global _start

# _start:
#     mov eax, 5      ; загрузить число 5 в регистр eax
#     add eax, 3      ; прибавить 3 к eax
#     mov ebx, eax    ; скопировать результат в ebx
#     mov eax, 1      ; системный вызов "exit"
#     int 0x80        ; прерывание для выхода
# """