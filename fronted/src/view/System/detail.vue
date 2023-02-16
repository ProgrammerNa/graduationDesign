<!--<script setup lang="ts">-->
<!--    import {ref, defineExpose, onMounted} from 'vue'-->
<!--    import {getUserDetailByUserId} from '../../api/systemApi'-->

<!--    const show = ref(false)-->
<!--    //点击详情该行的用户id-->
<!--    const rowId = ref(0)-->
<!--    const informational = ref([])-->
<!--    const open = (data: any) => {-->
<!--        if (data) {-->
<!--            show.value = data.show-->
<!--            rowId.value = data.info.id-->
<!--        }-->
<!--    }-->
<!--    const getDetailInfo = () => {-->
<!--        getUserDetailByUserId({-->
<!--            id: rowId.value-->
<!--        }).then((res) => {-->
<!--            if (res.status === 200) {-->
<!--                informational.value = res.data[0]-->
<!--            }-->
<!--        })-->
<!--    }-->
<!--    const init = () => {-->
<!--        getDetailInfo()-->
<!--    }-->
<!--    defineExpose({-->
<!--        open-->
<!--    })-->
<!--</script>-->


<!--<template>-->
<!--    <el-dialog-->
<!--            v-model="show"-->
<!--            title="用户信息详情"-->
<!--            width="50%"-->
<!--            align-center-->
<!--            @open="init"-->
<!--    >-->
<!--        <el-descriptions :column="1" border>-->
<!--            <el-descriptions-item-->
<!--                    label="用户名"-->
<!--            >{{informational.username}}-->
<!--            </el-descriptions-item-->
<!--            >-->
<!--            <el-descriptions-item-->
<!--                    label="用户名"-->
<!--            >{{informational.username}}-->
<!--            </el-descriptions-item-->
<!--            >-->
<!--        </el-descriptions>-->
<!--    </el-dialog>-->
<!--</template>-->


<!--<style scoped>-->

<!--</style>-->