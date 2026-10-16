"""
通讯录管理系统
功能：添加、显示、查询、修改、删除联系人，数据持久化存储（CSV格式）
"""

import csv
import os


class Contact:
    """联系人类，存储单个联系人的信息"""
    
    def __init__(self, name, phone, tag=""):
        """初始化联系人"""
        self.name = name.strip()
        self.phone = phone.strip()
        self.tag = tag.strip() if tag else ""
    
    def to_list(self):
        """将联系人对象转换为列表，用于CSV存储"""
        return [self.name, self.phone, self.tag]
    
    @classmethod
    def from_list(cls, data):
        """从列表创建联系人对象"""
        name = data[0] if len(data) > 0 else ""
        phone = data[1] if len(data) > 1 else ""
        tag = data[2] if len(data) > 2 else ""
        return cls(name=name, phone=phone, tag=tag)
    
    def display(self):
        """格式化显示联系人信息"""
        print(f"姓名：{self.name}")
        print(f"电话：{self.phone}")
        print(f"标签：{self.tag if self.tag else '未设置'}")
    
    def matches_keyword(self, keyword):
        """判断联系人是否匹配搜索关键词"""
        keyword = keyword.lower()
        return (keyword in self.name.lower() or
                keyword in self.phone.lower() or
                keyword in self.tag.lower())


class AddressBook:
    """通讯录管理类，负责联系人的增删改查和数据持久化"""
    
    def __init__(self, filename="contacts.csv"):
        """初始化通讯录"""
        self.filename = filename
        self.contacts = []
        self.load_contacts()
    
    def load_contacts(self):
        """从CSV文件加载联系人数据"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, "r", encoding="utf-8-sig") as file:
                    csv_reader = csv.reader(file)
                    first_row = next(csv_reader, None)
                    
                    if first_row and first_row == ['姓名', '电话', '标签']:
                        pass
                    elif first_row:
                        self.contacts.append(Contact.from_list(first_row))
                    
                    for row in csv_reader:
                        if row:
                            self.contacts.append(Contact.from_list(row))
            else:
                self.contacts = []
        except Exception as e:
            print(f"加载数据失败：{e}")
            self.contacts = []
    
    def save_contacts(self):
        """将联系人数据保存到CSV文件"""
        try:
            with open(self.filename, "w", encoding="utf-8-sig", newline="") as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(['姓名', '电话', '标签'])
                for contact in self.contacts:
                    csv_writer.writerow(contact.to_list())
            return True
        except Exception as e:
            print(f"保存失败：{e}")
            return False
    
    def add_contact(self, name, phone, tag=""):
        """添加新联系人"""
        for contact in self.contacts:
            if contact.name == name.strip():
                print(f"联系人已存在！")
                return False
        
        new_contact = Contact(name, phone, tag)
        self.contacts.append(new_contact)
        self.save_contacts()
        print("添加成功！")
        return True
    
    def display_all(self):
        """显示所有联系人"""
        if not self.contacts:
            print("通讯录为空")
            return
        
        print(f"\n{'='*40}")
        print(f"共 {len(self.contacts)} 个联系人")
        print(f"{'='*40}")
        
        for i, contact in enumerate(self.contacts, 1):
            print(f"\n【{i}】")
            contact.display()
    
    def search_contacts(self, keyword):
        """搜索联系人"""
        results = [c for c in self.contacts if c.matches_keyword(keyword)]
        
        if not results:
            print("未找到匹配的联系人")
            return []
        
        print(f"\n找到 {len(results)} 个联系人：")
        print("=" * 40)
        
        for i, contact in enumerate(results, 1):
            print(f"\n【{i}】")
            contact.display()
        
        return results
    
    def update_contact(self, name):
        """修改联系人信息"""
        for contact in self.contacts:
            if contact.name == name:
                print("当前信息：")
                contact.display()
                print("\n输入新信息（回车跳过）：")
                
                new_name = input("姓名：").strip()
                new_phone = input("电话：").strip()
                new_tag = input("标签：").strip()
                
                # 如果要修改姓名，检查新姓名是否已存在
                if new_name and new_name != name:
                    for c in self.contacts:
                        if c.name == new_name:
                            print("该姓名已存在！")
                            return False
                    contact.name = new_name
                
                if new_phone:
                    contact.phone = new_phone
                if new_tag:
                    contact.tag = new_tag
                
                self.save_contacts()
                print("修改成功！")
                return True
        
        print("联系人不存在！")
        return False
    
    def delete_contact(self, name):
        """删除联系人"""
        for i, contact in enumerate(self.contacts):
            if contact.name == name:
                contact.display()
                confirm = input("确认删除？(y/n)：").strip().lower()
                
                if confirm == 'y':
                    del self.contacts[i]
                    self.save_contacts()
                    print("删除成功！")
                    return True
                else:
                    print("已取消")
                    return False
        
        print("联系人不存在！")
        return False


class InputValidator:
    """输入验证类"""
    
    @staticmethod
    def validate_phone(phone):
        """验证电话号码格式"""
        if not phone.strip():
            return False
        cleaned = phone.replace(" ", "").replace("-", "").replace("+", "").replace("(", "").replace(")", "")
        if not cleaned:
            return False
        return True
    
    @staticmethod
    def get_valid_input(prompt, validator=None, error_msg="输入无效"):
        """获取有效用户输入"""
        while True:
            user_input = input(prompt).strip()
            if not user_input:
                print("输入不能为空！")
                continue
            if validator and not validator(user_input):
                print(error_msg)
                continue
            return user_input


class MenuSystem:
    """菜单系统类"""
    
    def __init__(self):
        self.address_book = AddressBook()
        self.validator = InputValidator()
    
    def clear_screen(self):
        """清屏"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_main_menu(self):
        """显示主菜单"""
        print("\n" + "=" * 30)
        print("       通讯录管理系统")
        print("=" * 30)
        print("1. 添加联系人")
        print("2. 显示联系人")
        print("3. 查询联系人")
        print("4. 修改联系人")
        print("5. 删除联系人")
        print("6. 保存数据")
        print("0. 退出")
        print("=" * 30)
    
    def handle_add_contact(self):
        """添加联系人"""
        print("\n--- 添加联系人 ---")
        
        name = self.validator.get_valid_input(
            "姓名：",
            error_msg="姓名不能为空！"
        )
        
        phone = self.validator.get_valid_input(
            "电话：",
            validator=self.validator.validate_phone,
            error_msg="电话格式不正确！"
        )
        
        tag = input("标签（回车跳过）：").strip()
        
        self.address_book.add_contact(name, phone, tag)
    
    def handle_search_contact(self):
        """搜索联系人"""
        if not self.address_book.contacts:
            print("通讯录为空")
            return
        
        print("\n--- 搜索联系人 ---")
        keyword = input("关键词：").strip()
        
        if not keyword:
            print("关键词不能为空！")
            return
        
        self.address_book.search_contacts(keyword)
    
    def handle_update_contact(self):
        """修改联系人"""
        if not self.address_book.contacts:
            print("通讯录为空")
            return
        
        print("\n--- 修改联系人 ---")
        name = input("请输入要修改的联系人姓名：").strip()
        
        if not name:
            print("姓名不能为空！")
            return
        
        self.address_book.update_contact(name)
    
    def handle_delete_contact(self):
        """删除联系人"""
        if not self.address_book.contacts:
            print("通讯录为空")
            return
        
        print("\n--- 删除联系人 ---")
        name = input("姓名：").strip()
        
        if not name:
            print("姓名不能为空！")
            return
        
        self.address_book.delete_contact(name)
    
    def run(self):
        """运行主程序"""
        while True:
            self.display_main_menu()
            
            try:
                choice = input("请选择：").strip()
                
                if choice == '1':
                    self.handle_add_contact()
                elif choice == '2':
                    self.address_book.display_all()
                elif choice == '3':
                    self.handle_search_contact()
                elif choice == '4':
                    self.handle_update_contact()
                elif choice == '5':
                    self.handle_delete_contact()
                elif choice == '6':
                    self.address_book.save_contacts()
                elif choice == '0':
                    self.address_book.save_contacts()
                    print("再见！")
                    break
                else:
                    print("无效选择")
                
                if choice != '0':
                    input("\n按回车继续...")
                    self.clear_screen()
                    
            except KeyboardInterrupt:
                print("\n正在保存...")
                self.address_book.save_contacts()
                break
            except Exception as e:
                print(f"错误：{e}")
                input("按回车继续...")


def main():
    """主函数"""
    try:
        menu_system = MenuSystem()
        menu_system.run()
    except Exception as e:
        print(f"程序错误：{e}")
        input("按回车退出...")


if __name__ == "__main__":
    main()
