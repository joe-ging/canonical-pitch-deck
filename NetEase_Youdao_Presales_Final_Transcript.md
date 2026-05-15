# NetEase Youdao Hybrid Cloud Pitch — Final Transcript

> Consultative presales pitch by Margot (Canonical MLOps Field Engineer)
> Tone: Partnership "we" — never accusatory "you"

---

## Slide 0: Cover - Strategic Proposal

Good morning, everyone. Thank you for making time for this strategic review. I am Margot, an MLOps Field Engineer here at Canonical. Today, our team wants to walk through a pivotal shift in the infrastructure (/ˈɪn.frə.strʌk.tʃər/) roadmap at NetEase Youdao. As the platform has scaled to become a leading AI-driven learning system, it has arrived at a critical crossroads. The public cloud served the business well during hyper-growth, but as annual video streaming traffic hits eighteen Petabytes—equivalent to streaming high-definition video non-stop for over a thousand years—the 'convenience' of the cloud is becoming a strategic liability. We aren't here to dismantle what's been built, but to evolve it. Canonical is proposing a transition to a managed private cloud—a Hybrid model—that ensures NetEase Youdao owns its future, its margins, and its data.

---

## Slide 1: 01. Understanding Your Scale

Let me walk everyone through the scale of this operation. With over five million registered students, NetEase Youdao is in the top tier of APAC EdTech. During peak hours—4 PM to 9 PM every day—the platform handles four hundred and twenty thousand students online at the same time. That is nearly half a million students relying on the system for real-time education. The traffic splits: 70% is in large classes with hundreds of students watching one teacher, which require immense processing power to convert video formats in real-time. The remaining 30% are small interactive groups. To the leaders in the room, this isn't just data; it's a living, breathing media factory that requires a foundation built for maximum efficiency and rock-solid reliability.

---

## Slide 2: 02. Understanding Your Operations

The operation is defined by this massive daily pulse. From 4 PM onwards, the workload spikes to over fifty thousand cores. Imagine the processing power needed to run a mid-sized city's entire digital infrastructure—that is the scale we're talking about. Currently, this peak is managed primarily on the public cloud. However, this 'pulse' is very predictable. In the public cloud, we pay for flexibility—the ability to scale for the unknown. But we know the peaks. The business is essentially paying a premium for a level of uncertainty that doesn't exist in this model. On top of that, the massive monthly video traffic is a constant drain on resources.

---

## Slide 3: 03. Your Requirements

What does the engineering team need to deliver? Videos need to start playing within half a second to keep student engagement. The system needs rock-solid connections for interactive small groups. And most importantly, it needs high-quality 1080p video processing. The business needs are just as rigorous: zero-downtime maintenance and strict data compliance across China, Hong Kong, and Singapore. Currently, these needs are being met, but at a cost that is eating into the R&D budget. The real question is: can we achieve the same performance while significantly lowering the cost per minute of video?

---

## Slide 4: 04. The Problem

The core problem is what I call the 'Public Cloud Trap.' In a pure public cloud model, infrastructure costs grow in lockstep with student count. On AWS or Azure, every new student adds a predictable, fixed amount of processing and bandwidth cost that cannot be optimized further. Because these providers charge 'retail' rates, a business at this scale is effectively subsidizing their profit margins. Using public cloud for this level of video processing is like renting a private jet just to deliver the morning mail. It works, but the math just doesn't add up at this stature. We need to break the link between adding students and adding costs.

---

## Slide 5: 05. Workload: Tier 1

Let's talk about the biggest expense: Video Processing. This single task accounts for 74% of total processing needs—over forty thousand cores at peak. The platform takes a single video feed from a teacher and converts it into multiple formats so students with different internet speeds can watch smoothly. Doing this heavy video processing on general-purpose cloud servers is extremely expensive. Public clouds charge for the abstraction, but processing video is pure math that runs better on physical machines with dedicated hardware designed specifically for video. This is the single biggest lever for cost savings—and it's the easiest to move.

---

## Slide 6: 06. Workload: Tiers 2-5

The remaining 26% of the workload is split between media signaling, the software layer that manages logins, scheduling, and payments, the databases, and the AI systems. Tiers 2 and 3 are critical for interactivity. Tier 4 is the source of truth, requiring highly stable database servers. Finally, Tier 5 is the 'Secret Sauce'—the AI models that power personalized learning. Currently, these are all scattered across cloud servers. Our proposal is to bring the processing power for these tiers into a dedicated private infrastructure while keeping the public cloud as a backup. If the main servers ever get too busy, the system simply falls back to the public cloud, ensuring classes never go offline.

---

## Slide 7: 07. Infrastructure Summary

To summarize the total footprint: over fifty thousand cores, five hundred terabytes of hot storage, five Petabytes of archival storage, and eighteen Petabytes of annual video traffic. These are 'Tier-1' numbers. At this level, the organization is no longer a 'customer' of the cloud; it is essentially building the cloud for someone else. 74% of the processing is video, and the video streaming cost is the single largest line item in the bandwidth bill. For NetEase Youdao, the message is clear: the scale has surpassed the point where 'renting' is cheaper than 'owning.' It is time to treat infrastructure as a capital asset rather than a monthly subscription expense. So the question becomes: who can help us build this?

---

## Slide 8: 08. Who is Canonical?

That's where we come in. Canonical is the global authority in open source. Ubuntu is the foundation for 70% of public cloud workloads and 100% of 5G mobile networks. We are the number one operating system for public cloud and the number one OpenStack distributor, trusted by organizations like NASA, AT&T, and Bloomberg. This isn't just buying software; it's partnering with the experts who build the foundation of the modern internet. Let me show exactly how the technology works.

---

## Slide 9: 09. The Charmed Stack

At the bottom, MAAS gives absolute control over the physical hardware. Above that, Charmed OpenStack is the layer that turns physical servers into flexible virtual machines. Finally, Charmed Kubernetes runs the modern software services on top. The beauty of this stack is its 'Charm' architecture—every component is managed by a software operator that automates the hard parts. This isn't a DIY project; it's a professionally engineered, fully managed private cloud. We get the performance of dedicated machines with the orchestration (/ˌɔː.kɪˈstreɪ.ʃən/) of the modern cloud.

---

## Slide 10: 10. The Economics of Freedom

One of the most frustrating aspects of the public cloud is unpredictable billing. Hidden fees make budgeting a nightmare. Canonical offers the economics of freedom. A fixed price per machine per year for managed operations, with zero proprietary license fees and zero lock-in. A traditional 'per-core' tax would increase costs by 300% as we add more power. After Broadcom acquired VMware and raised prices dramatically, many companies are looking for alternatives. Canonical provides an open, predictable path. So what does this look like in practice for NetEase Youdao?

---

## Slide 11: 11. The Proposal

I want to be clear: we are not suggesting abandoning the public cloud. Instead, we propose a Hybrid model. We move 88% of the workload—the predictable, high-traffic loads and sensitive databases—to a Canonical-managed private cloud. We keep 12% on the public cloud as a safety net for unpredictable spikes. AWS stays as the safety net, not the primary bill.

---

## Slide 12: 12. Workload Allocation

How do we split things up? We prioritize predictability and compliance (/kəmˈplaɪ.əns/). The core video processing, databases containing sensitive student information, and AI systems all move entirely to the private cloud. Only the overflow capacity for unexpected spikes remains on the public cloud. That 12% on the public cloud automatically scales up and down, meaning it costs zero when it isn't being used. The AWS bill drops dramatically.

---

## Slide 13: 13. Zero-Downtime Migration

The biggest fear is always downtime. We use a 'Shadow Run' strategy. We build the private cloud entirely in parallel—the existing system keeps running untouched. Then, we mirror 10% of traffic, gradually shifting to 100% over 8 weeks. If we see any issues at any point, the system automatically falls back to AWS within 60 seconds. Students never notice. Teachers never notice. The transition happens entirely behind the scenes. Zero downtime. Zero risk to service commitments.

---

## Slide 14: 14. The Real Cost Drivers

\

---

## Slide 15: 15. Honest Comparison

Let's look at the annual cost. AWS Reserved is twelve point seven million dollars. AWS with Kubernetes elasticity (/ˌiː.læsˈtɪs.ɪ.ti/) only drops to eleven point six million because the video traffic and storage costs remain completely unchanged at three point one million. The Canonical private cloud drops the annual total to roughly six point one million. Video traffic cost drops to essentially zero, storage is free on owned disks, and AI training is a free bonus using idle hardware. That is more than half off compared to AWS. And cost isn't even the only reason to make this move.

---

## Slide 16: 16. Data Sovereignty & Compliance

In APAC, compliance (/kəmˈplaɪ.əns/) is mandatory. With PIPL in China, student data must reside on local soil. Penalties for violations can reach up to 5% of annual revenue. A private cloud gives physical control—the organization's own servers, own datacenter, own jurisdiction. Data never leaves the sovereign (/ˈsɒv.rɪn/) infrastructure. And with Canonical's Ubuntu Pro, we provide audit-ready environments with federal-grade security certification and zero-downtime security patching. Let me put all of this into concrete numbers.

---

## Slide 17: 17. The Numbers

Over three years, staying on AWS will cost nearly forty million dollars. Google and Azure are similar. The 3-year Total Cost of Ownership (/ˈtoʊ.təl kɔːst əv ˈoʊ.nər.ʃɪp/) with Canonical, including the upfront hardware purchase and three years of managed operations, comes to just over eighteen million. That is a saving of twenty-one point four million dollars—more than half off versus AWS.

---

## Slide 18: 18. Financial Proof

Looking at the cumulative graph, the cross-over point is early in Year 2. After the initial hardware purchase in Year 1, operating costs stay completely flat—the same amount, year after year. Meanwhile, staying on the public cloud means costs just keep climbing, month after month, with no end in sight.

---

## Slide 19: 19. Cost Breakdown

Where does the money go? On AWS, processing power alone is nearly twenty-nine million, and the fees for video traffic out to students is nearly five million over three years. With Canonical, the hardware is purchased once for eight point eight million, and we pay nine point six million for three years of around-the-clock managed operations. The video traffic and storage? Completely free—because the data travels over the organization's own network and sits on its own disks. Now, how do we actually make this happen?

---

## Slide 20: 20. Delivering Success

We follow a Build, Operate, Transfer model. First, Canonical builds the cloud. Then we operate it with a ninety-nine point nine percent uptime guarantee—that means less than nine hours of downtime in an entire year. At the same time, we train the internal team. Like Nayatel (/naɪ.jəˈtel/) in Pakistan, the organization eventually takes full control, dropping ongoing operations cost to zero. This is a clear path to independence, not vendor lock-in.

---

## Slide 21: RECLAIM CONTROL.

NetEase Youdao has an opportunity to save twenty-one point four million dollars and gain 100% data sovereignty (/ˈsɒv.rɪn.ti/). We recommend starting a 4-week Architecture Audit together to begin this journey. Let's reclaim control. Thank you.

---

