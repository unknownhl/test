#!/usr/bin/env python
# _*_ coding: utf-8 _*_
'''
=================================================
@Project -> File   ：template -> crawl
@IDE    ：PyCharm
@Author ：Huang Li
@Date   ：2022/4/1 12:52
@Desc   ：
==================================================
'''
import json
from urllib.request import Request
from urllib.request import urlopen

import jsonlines


def get_project_labels(owner, name, headers):
    url = 'https://api.github.com/repos/{owner}/{name}'.format(owner=owner, name=name)
    req = Request(url, headers=headers)
    response = urlopen(req).read()
    if len(response) == 0:
        return response
    else:
        result = json.loads(response.decode())
        return result['topics']


if __name__ == '__main__':
    project_list = []
    tmp_dict = {}
    with open("D:\\PyCharmProject\\plpi\\data\\PLPI_GitHub_dataset.txt", 'r', encoding='utf-8') as f:
        for each_line in f:
            json_obj = json.loads(each_line)
            # print(json_obj["project"])
            project_list.append(json_obj["project"])

    result = list(set(project_list))
    print(len(result))
    print(len(set(project_list)))
    headers = {'User-Agent': 'Mozilla/5.0',
               'Authorization': 'token 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',
               'Content-Type': 'application/json',
               'Accept': 'application/json'
               }
    # token
    '''
    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
    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
    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
    '''

    for project in result:
        owner = str(project).split('_')[0]
        name = str(project).split('_')[1]
        try:
            labels = get_project_labels(owner, name, headers)
            tmp_dict.update({
                "project": project,
                "labels": labels
            })
            with jsonlines.open("D:\\PyCharmProject\\plpi\\data\\projects_info.jsonl", mode='a') as writer:
                writer.write(tmp_dict)
            tmp_dict.clear()
        except:
            print(project, '|' + owner, '|', name)