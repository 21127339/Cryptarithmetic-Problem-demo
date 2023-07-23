import string

class Number:
    
    def __init__(self, str_form, len, sign):
        self.str_form = str_form
        self.len = len
        self.sign = sign 
        
    def Fix(self, MAX_LEN):
        if len(self.str_form) < MAX_LEN:
            for _ in range(MAX_LEN - self.len):
                self.str_form = '*' + self.str_form
                
def AnalysInput(input = string):
    size = len(input)
    variables = []
    for i in range(size):
        if input[i] >= 'A' and input[i] <= 'Z':
            if input[i] not in variables:
                variables.append(input[i])
    if(len(variables) >= 10):
        return False
    #Kiểm tra số chữ cái có hợp lệ hay không
    
    reverse = 0
    #Biến lưu dấu trước dấu ngoặc
    data = ""
    
    for i in range(size):
    #Tạo phép tính không có dấu ngoặc  
        if input[i] == '(':
            if i != 0 and input[i - 1] == '-':
                reverse = 1
        #Nếu có dấu '-' trước dấu ngoặc thì bắt đầu đổi dấu
        
        elif input[i] == ')':
            reverse = 0
        #Kết thúc đổi dấu    
        
        elif input[i] == '+' and reverse == 1:
            data += '-'
        elif input[i] == '-' and reverse == 1:
            data += '+'
        #Đổi dấu sau dấu ngoặc
        
        else:
            data += input[i]
    
    size = len(data)
    operands = [] 
    answer = None
    start = 0
    temp = ""
    
    for i in range(size):
    #Chia các toán hạng và dấu của chúng    
        if data[i] == '+':
            temp = data[start: i : 1]
            operands.append(Number(temp, len(temp), 1))
            print(temp, i)
            start = i + 1
        elif data[i] == '-':
            temp = data[start: i: 1]
            operands.append(Number(temp, len(temp), -1))
            print(temp, i)    
            start = i + 1  
        elif data[i] == '=':
            temp = data[start: i: 1]
            sign = 1
            if data[start - 1] == '-': sign = -1
            operands.append(Number(temp, len(temp), sign))
            print(temp, sign)    
            start = i + 1
            temp = data[start:]
            answer = Number(temp, len(temp), 1)
            print(temp) 
    
    nonZero = set()
    for i in operands:
        if i.str_form[0] not in nonZero:
            nonZero.add(i.str_form[0])
            
    MAX_LEN = 0
    for i in operands:
        MAX_LEN = max(MAX_LEN, i.len)
    MAX_LEN = max(MAX_LEN, answer.len)
    print(MAX_LEN)    
    for i in operands:
        for _ in range(MAX_LEN - i.len):
            i.str_form = '*' + i.str_form
        print(i.str_form)
    for _ in range(MAX_LEN - answer.len):
        answer.str_form = '*' + answer.str_form 
    print(answer.str_form) 
    #Đưa các toán hạng về cùng 1 dạng
              
    return operands, answer, variables, nonZero

def IsValid(operands, answer, nonZero, col, currentState, carry):
    sum = 0
    state = currentState.copy()
    
    for i in operands:
        if i.str_form[col] != '*':
            value = state[i.str_form[col]]
            sum += value * i.sign
    
    if ((sum + carry) % 10) == 0 and answer.str_form[col] in nonZero:
        return False
    if state[answer.str_form[col]] == None:
        if ((sum + carry) % 10) not in state.values():
            state[answer.str_form[col]] = (sum + carry) % 10
            newCarry = (sum + carry) // 10
            return newCarry, state
        return False
    else:
        if (sum + carry) % 10 == state[answer.str_form[col]]:
            newCarry = (sum + carry) // 10
            return newCarry, state
        return False
    
def ForwardChecking(operands, answer, nonZero, col, opr_i , currentState, carry):
    variable = operands[opr_i].str_form[col]
    state = currentState.copy()
    
    print(variable)
    if variable != '*' and state[variable] == None:
        for k in range(10):
            if k == 0 and variable in nonZero:
                continue
            if k in state.values():
                continue
            print(variable, k)
            state[variable] = k
            if opr_i == len(operands) - 1:
                if IsValid(operands, answer, nonZero, col, state, carry) != False: 
                    newCarry, newState = IsValid(operands, answer, nonZero, col, state, carry)
                    print("Success")
                    if ForwardChecking(operands, answer, nonZero, col - 1, 0 , newState, carry) != False:
                        return True
            else:
                check = ForwardChecking(operands, answer, nonZero, col, opr_i + 1 , state, carry)
                if check == True:
                    return True
    else:       
        if opr_i == len(operands) - 1:
            if IsValid(operands, answer, nonZero, col, state, carry) != False: 
                newCarry, newState = IsValid(operands, answer, nonZero, col, state, carry)
                if newCarry == 0 and col == 0:    
                    print("Fck success")
                    print(newState)
                    return True
                if newCarry != False: 
                    print("Success")
                    if ForwardChecking(operands, answer, nonZero, col - 1, 0 , newState, newCarry) != False:
                            return True
        else:
            check = ForwardChecking(operands, answer, nonZero, col, opr_i + 1 , state, carry)
            if check == True:
                return True 
    return False

def Solve(operands, answer, variables, nonZero):
    n = len(answer.str_form)
    state = dict()  
    for i in variables:
        state.update({i: None})
    #state.update({'*': 0})
    check = ForwardChecking(operands, answer, nonZero, n - 1, 0, state, 0)

def main():
    operands, answer, variables, nonZero = AnalysInput("ABCD+DE=DEFG")
    Solve(operands, answer, variables, nonZero)       
main()