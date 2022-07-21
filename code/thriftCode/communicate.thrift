const i32 CAPPING = 1
const i32 UNCAPPING = 0

service Communicate {
    string connect_test(),
    i32 sayMsg(1:i32 capping_type, 2:double capping_target, 3:i32 capping_id)
}