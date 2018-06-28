# 日志选择

## 常见的在java中使用的日志有如下几种：

1. log4j
Log4j = Log for Java.
author: Ceki Gülcü
Log4j是Apache的一个开放源代码项目，通过使用Log4j，我们可以控制日志信息输送的目的地是控制台、文件、数据库等；我们也可以控制每一条日志的输出格式；通过定义每一条日志信息的级别，我们能够更加细致地控制日志的生成过程。
Log4j有7种不同的log级别，按照等级从低到高依次为：TRACE<DEBUG<INFO<WARN<ERROR<FATAL<OFF。如果配置为OFF级别，表示关闭log。
Log4j支持两种格式的配置文件：properties和xml。包含三个主要的组件：Logger、appender、Layout。 

2. log4j2
已经有很多其他的日志框架对Log4j进行了改良，比如说SLF4J、Logback等。而且Log4j 2在各个方面都与Logback非常相似，那么为什么我们还需要Log4j 2呢？
插件式结构。Log4j 2支持插件式结构。我们可以根据自己的需要自行扩展Log4j 2. 我们可以实现自己的appender、logger、filter。
配置文件优化。在配置文件中可以引用属性，还可以直接替代或传递到组件。而且支持json格式的配置文件。不像其他的日志框架，它在重新配置的时候不会丢失之前的日志文件。
Java 5的并发性。Log4j 2利用Java 5中的并发特性支持，尽可能地执行最低层次的加锁。解决了在log4j 1.x中存留的死锁的问题。如果你的程序仍然在饱受内存泄露的折磨，请毫不犹豫地试一下log4j 2吧。
异步logger。Log4j 2是基于LMAX Disruptor库的。在多线程的场景下，和已有的日志框架相比，异步的logger拥有10左右的效率提升。
还有更多的新特性，在这里就不一一赘述了。了解更多请移步到：http://logging.apache.org/log4j/2.x/manual/index.html


3. slf4j
SLF4J = Simple Logging Facade for Java.
author： Ceki Gülcü
SLF4J，即简单日志门面（Simple Logging Facade for Java），不是具体的日志解决方案，而是通过Facade Pattern提供一些Java logging API，它只服务于各种各样的日志系统。按照官方的说法，SLF4J是一个用于日志系统的简单Facade，允许最终用户在部署其应用时使用其所希望的日志系统。作者创建SLF4J的目的是为了替代Jakarta Commons-Logging。
实际上，SLF4J所提供的核心API是一些接口以及一个LoggerFactory的工厂类。在使用SLF4J的时候，不需要在代码中或配置文件中指定你打算使用那个具体的日志系统。SLF4J提供了统一的记录日志的接口，只要按照其提供的方法记录即可，最终日志的格式、记录级别、输出方式等通过具体日志系统的配置来实现，因此可以在应用中灵活切换日志系统。
那么什么时候使用SLF4J比较合适呢？
如果你开发的是类库或者嵌入式组件，那么就应该考虑采用SLF4J，因为不可能影响最终用户选择哪种日志系统。在另一方面，如果是一个简单或者独立的应用，确定只有一种日志系统，那么就没有使用SLF4J的必要。假设你打算将你使用log4j的产品卖给要求使用JDK 1.4 Logging的用户时，面对成千上万的log4j调用的修改，相信这绝对不是一件轻松的事情。但是如果开始便使用SLF4J，那么这种转换将是非常轻松的事情。

4. logback
author： Ceki Gülcü
licences：EPL v1.0 and LGPL 2.1
Logback，一个“可靠、通用、快速而又灵活的Java日志框架”。logback当前分成三个模块：logback-core，logback- classic和logback-access。logback-core是其它两个模块的基础模块。logback-classic是log4j的一个改良版本。此外logback-classic完整实现SLF4J API使你可以很方便地更换成其它日志系统如log4j或JDK14 Logging。logback-access访问模块与Servlet容器集成提供通过Http来访问日志的功能。
logback-core: Joran, Status, context, pattern parsing
logback-classic: developer logging
logback-access: The log generated when a user accesses a web-page on a web server. Integrates seamlessly with Jetty and Tomcat.
选择logback的理由：（http://logback.qos.ch/reasonsToSwitch.html#fasterImpl ）
logback比log4j要快大约10倍，而且消耗更少的内存。
logback-classic模块直接实现了SLF4J的接口，所以我们迁移到logback几乎是零开销的。
logback不仅支持xml格式的配置文件，还支持groovy格式的配置文件。相比之下，Groovy风格的配置文件更加直观，简洁。
logback-classic能够检测到配置文件的更新，并且自动重新加载配置文件。
logback能够优雅的从I/O异常中恢复，从而我们不用重新启动应用程序来恢复logger。
logback能够根据配置文件中设置的上限值，自动删除旧的日志文件。
logback能够自动压缩日志文件。
logback能够在配置文件中加入条件判断（if-then-else)。可以避免不同的开发环境（dev、test、uat...）的配置文件的重复。
logback带来更多的filter。
logback的stack trace中会包含详细的包信息。
logback-access和Jetty、Tomcat集成提供了功能强大的HTTP-access日志。
配置文件：需要在项目的src目录下建立一个logback.xml。注：（1）logback首先会试着查找logback.groovy文件；（2）当没有找到时，继续试着查找logback-test.xml文件；（3）当没有找到时，继续试着查找logback.xml文件；（4）如果仍然没有找到，则使用默认配置（打印到控制台）。 详细的配置在http://aub.iteye.com/blog/1101222 这篇博客中解释的非常清楚。在这里感谢一下原作者（^_^）。

5. jcl
JCL = Jakarta Commons-Logging.
Jakarta Commons Logging和SLF4J非常类似，也是提供的一套API来掩盖了真正的Logger实现。便于不同的Logger的实现的替换，而不需要重新编译代码。缺点在于它的查找Logger的实现者的算法比较复杂，而且当出现了一些class loader之类的异常时，无法去修复它。

6. jul
JUL = java.util.logging.
Java提供了自己的日志框架，类似于Log4J，但是API并不完善，对开发者不是很友好，而且对于日志的级别分类也不是很清晰，比如：SEVERE, WARNING, INFO, CONFIG, FINE,FINER, FINEST。所以不推荐使用这种方式输出日志。

## 我们为什么选择log4j2

有这么多类型的日志，我们为什么选择log4j2

1. log4j在多线程下情况会产生死锁。
2. log4j2在异步情况下，64核性能是普通log的10倍。
3. log4j2和log4j是一个作者，只不过log4j2是重新架构的一款日志组件，他抛弃了之前log4j的不足，以及吸取了优秀的logback的设计重新推出的一款新组件。
4. 对于我们来说，从log4j迁移到log4j2只要简单，不出问题，然后性能还可以，就能接受。
